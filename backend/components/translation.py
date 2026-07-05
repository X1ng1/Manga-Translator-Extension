from transformers import Mistral3ForConditionalGeneration, MistralCommonBackend, FineGrainedFP8Config
from typing import List, Tuple, Dict, Union
import json
import re
import torch

MODEL_ID = "mistralai/Ministral-3-3B-Instruct-2512"

_tokenizer = None
_model = None


def _get_model():
    global _tokenizer, _model
    if _model is None:
        print("Loading model...")
        _tokenizer = MistralCommonBackend.from_pretrained(MODEL_ID)
        _model = Mistral3ForConditionalGeneration.from_pretrained(
            MODEL_ID,
            device_map="auto",
            quantization_config=FineGrainedFP8Config(),
            offload_folder="offload_cache",
            torch_dtype = torch.bfloat16
        )
        print("Model ready")
    return _tokenizer, _model


def translate_text(text_with_bubbles: List[Dict[str, Union[Tuple[int, int, int, int], str]]]):
    tokenizer, model = _get_model()

    numbered_texts = "\n".join(
        f"[{i}] {bubble['text']}"
        for i, bubble in enumerate(text_with_bubbles)
    )

    SYSTEM_PROMPT = """You are an expert manga translator.

    Translate Japanese manga dialogue into natural English.

    You will receive numbered speech bubbles from a single manga page.
    Translate ALL of them together to preserve context, tone, and flow.

    Preserve:
    - Tone
    - Emotion
    - Character personality
    - Reading order and context between bubbles

    Return ONLY a JSON object mapping each bubble number to its translation.
    Example format:
    {"0": "translation of bubble 0", "1": "translation of bubble 1"}

    Do not include anything else in your response."""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": numbered_texts}
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        max_length=None,
        do_sample=False
    )

    response = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True
    ).strip()

    translations = _parse_translation_response(response, len(text_with_bubbles))

    return [
        {
            "bbox": bubble["bbox"],
            "original": bubble["text"],
            "translation": translations.get(i, bubble["text"]),
        }
        for i, bubble in enumerate(text_with_bubbles)
    ]


def _parse_translation_response(response: str, expected_count: int) -> Dict[int, str]:
    cleaned = re.sub(r"^```[a-zA-Z]*\n?|```$", "", response.strip(), flags=re.MULTILINE).strip()

    try:
        parsed = json.loads(cleaned)
        return {int(k): v for k, v in parsed.items()}
    except json.JSONDecodeError:
        pass

    matches = re.findall(r'"?(\d+)"?\s*:\s*"([^"]*)"', cleaned)
    if matches:
        return {int(k): v for k, v in matches}

    if expected_count == 1:
        return {0: response}

    return {}