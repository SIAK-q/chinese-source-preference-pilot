"""Load the selected model families and read conditional first-step probabilities.

Gemma 4 uses its multimodal processor/model even for text-only input, with
thinking disabled. Moonlight's custom code is pinned to the reviewed revision.
This adapter does not change the historical inference scripts.
"""
PINNED = {
    "Qwen/Qwen2.5-7B-Instruct": "a09a35458c702b33eeacc393d103063234e8bc28",
    "Qwen/Qwen2.5-14B-Instruct": "cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8",
    "Qwen/Qwen2.5-32B-Instruct": "5ede1c97bbab6ce5cda5812749b4c0bdf79b18dd",
    "Qwen/Qwen2.5-72B-Instruct": "495f39366efef23836d0cfae4fbe635880d2be31",
    "google/gemma-4-12B-it": "43c9d014b231474fa7212dbb48a762566c2b255d",
    "moonshotai/Moonlight-16B-A3B-Instruct": "4e735b07a89f73647dfab71ab91b840f362ede5b",
    # 11-05 用户定 3–8B 范围后新增（Hugging Face API sha，2026-11-05）
    "google/gemma-4-E4B-it": "4ecc2ba63bcac23ba4a767fc87025b1450f84c9c",
    "meta-llama/Llama-3.1-8B-Instruct": "0e9e39f249a16976918f6564b8830bc894c89659",
    # 11-08：Kimi-Linear 版本与 Codex 小测记录一致（models/work_records/2026-11-07-kimi-linear-readiness/）
    "moonshotai/Kimi-Linear-48B-A3B-Instruct": "e1df551a447157d4658b573f9a695d57658590e9",
}


class ModelBundle:
    def __init__(self, model_id, revision=None, dtype="auto", device_map="", local_only=False):
        import torch
        import transformers
        self.torch = torch
        self.transformers_version = transformers.__version__
        self.model_id = model_id
        self.revision = revision or PINNED.get(model_id)
        self.gemma = model_id.startswith("google/gemma-4-")
        remote = model_id.startswith("moonshotai/")
        major = int(transformers.__version__.split(".", 1)[0])
        if remote:
            import tiktoken  # Required by the pinned Moonshot tokenizers (Moonlight, Kimi-Linear).
        common = {"local_files_only": local_only}
        if self.revision:
            common["revision"] = self.revision
        if remote:
            common.update(trust_remote_code=True, code_revision=self.revision)
        if self.gemma:
            from transformers import AutoProcessor, AutoModelForMultimodalLM
            self.processor = AutoProcessor.from_pretrained(model_id, **common)
            self.tokenizer = self.processor.tokenizer
            cls = AutoModelForMultimodalLM
        else:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            self.processor = self.tokenizer = AutoTokenizer.from_pretrained(model_id, **common)
            cls = AutoModelForCausalLM
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "left"
        device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        selected_dtype = dtype
        if dtype == "auto" and device == "mps":
            selected_dtype = "float16"
        dtype_key = "dtype" if major >= 5 else "torch_dtype"
        kwargs = {**common, dtype_key: selected_dtype if selected_dtype == "auto" else getattr(torch, selected_dtype)}
        if device_map:
            kwargs["device_map"] = device_map
        self.model = cls.from_pretrained(model_id, **kwargs)
        if not device_map:
            self.model.to(device)
        self.model.eval()
        self.device = next(self.model.parameters()).device

    def prompt(self, system, user):
        kwargs = {"enable_thinking": False} if self.gemma else {}
        return self.processor.apply_chat_template(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            tokenize=False, add_generation_prompt=True, **kwargs)

    def probabilities(self, system, users, letters=("A", "B")):
        torch = self.torch
        ids = [self.tokenizer.encode(x, add_special_tokens=False) for x in letters]
        if any(len(x) != 1 for x in ids) or len({x[0] for x in ids}) != len(ids):
            raise ValueError(f"Answer letters are not distinct single tokens: {dict(zip(letters, ids))}")
        chats = [[{"role": "system", "content": system}, {"role": "user", "content": user}] for user in users]
        kwargs = {"enable_thinking": False} if self.gemma else {}
        batch = self.processor.apply_chat_template(chats, tokenize=True, return_dict=True,
                                                   return_tensors="pt", padding=True,
                                                   add_generation_prompt=True, **kwargs).to(self.device)
        with torch.inference_mode():
            output = self.model.generate(**batch, max_new_tokens=1, do_sample=False,
                                         return_dict_in_generate=True, output_scores=True,
                                         pad_token_id=self.tokenizer.pad_token_id)
        logits = output.scores[0][:, [x[0] for x in ids]].float()
        probabilities = torch.softmax(logits, dim=-1).cpu().tolist()
        generated = output.sequences[:, batch["input_ids"].shape[1]:]
        decoded = self.tokenizer.batch_decode(generated, skip_special_tokens=False)
        return probabilities, decoded

    def metadata(self):
        return {"model": self.model_id, "revision_requested": self.revision,
                "revision_resolved": getattr(self.model.config, "_commit_hash", None),
                "architecture": type(self.model).__name__, "device": str(self.device),
                "dtype": str(self.model.dtype), "torch": self.torch.__version__,
                "transformers": self.transformers_version,
                "thinking_disabled": self.gemma,
                "custom_code": self.model_id.startswith("moonshotai/")}
