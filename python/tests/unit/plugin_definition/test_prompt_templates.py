# Copyright (c) Microsoft. All rights reserved.

import json

import pytest

from semantic_kernel.connectors.ai.open_ai.models.chat.open_ai_chat_message import (
    OpenAIChatMessage,
)
from semantic_kernel.connectors.ai.open_ai.request_settings.open_ai_request_settings import (
    OpenAIChatRequestSettings,
)
from semantic_kernel.semantic_functions.chat_prompt_template import ChatPromptTemplate
from semantic_kernel.semantic_functions.prompt_template_config import (
    PromptTemplateConfig,
)
from semantic_kernel.template_engine.prompt_template_engine import PromptTemplateEngine


def test_default_prompt_template_config():
    prompt_template_config = PromptTemplateConfig()
    assert prompt_template_config.schema_ == 1
    assert prompt_template_config.type == "completion"
    assert prompt_template_config.description == ""
    assert prompt_template_config.execution_settings.extension_data == {}


def test_default_chat_prompt_template_from_empty_dict():
    prompt_template_config = PromptTemplateConfig.from_dict({})
    assert prompt_template_config.schema_ == 1
    assert prompt_template_config.type == "completion"
    assert prompt_template_config.description == ""
    assert prompt_template_config.execution_settings.extension_data == {}


def test_default_chat_prompt_template_from_empty_string():
    with pytest.raises(json.decoder.JSONDecodeError):
        _ = PromptTemplateConfig.from_json("")


def test_default_chat_prompt_template_from_empty_json():
    prompt_template_config = PromptTemplateConfig.from_dict({})
    assert prompt_template_config.schema_ == 1
    assert prompt_template_config.type == "completion"
    assert prompt_template_config.description == ""
    assert prompt_template_config.execution_settings.extension_data == {}


def test_custom_prompt_template_config():
    prompt_template_config = PromptTemplateConfig(
        schema_=2,
        type="completion2",
        description="Custom description.",
        execution_settings=OpenAIChatRequestSettings(
            temperature=0.5,
            top_p=0.5,
            presence_penalty=0.5,
            frequency_penalty=0.5,
            max_tokens=128,
            number_of_responses=2,
            stop=["\n"],
            logit_bias={"1": 1.0},
        ),
    )
    assert prompt_template_config.schema_ == 2
    assert prompt_template_config.type == "completion2"
    assert prompt_template_config.description == "Custom description."
    assert prompt_template_config.execution_settings.temperature == 0.5
    assert prompt_template_config.execution_settings.top_p == 0.5
    assert prompt_template_config.execution_settings.presence_penalty == 0.5
    assert prompt_template_config.execution_settings.frequency_penalty == 0.5
    assert prompt_template_config.execution_settings.max_tokens == 128
    assert prompt_template_config.execution_settings.number_of_responses == 2
    assert prompt_template_config.execution_settings.stop == ["\n"]
    assert prompt_template_config.execution_settings.logit_bias == {"1": 1.0}


def test_custom_prompt_template_config_from_dict():
    prompt_template_dict = {
        "schema": 2,
        "type": "completion2",
        "description": "Custom description.",
        "execution_settings": {
            "default": {
                "temperature": 0.5,
                "top_p": 0.5,
                "presence_penalty": 0.5,
                "frequency_penalty": 0.5,
                "max_tokens": 128,
                "number_of_responses": 2,
                "stop": ["\n"],
                "logit_bias": {"1": 1},
            },
        },
    }
    prompt_template_config = PromptTemplateConfig.from_dict(prompt_template_dict)
    assert prompt_template_config.schema_ == 2
    assert prompt_template_config.type == "completion2"
    assert prompt_template_config.description == "Custom description."
    assert prompt_template_config.execution_settings.extension_data["temperature"] == 0.5
    assert prompt_template_config.execution_settings.extension_data["top_p"] == 0.5
    assert prompt_template_config.execution_settings.extension_data["presence_penalty"] == 0.5
    assert prompt_template_config.execution_settings.extension_data["frequency_penalty"] == 0.5
    assert prompt_template_config.execution_settings.extension_data["max_tokens"] == 128
    assert prompt_template_config.execution_settings.extension_data["number_of_responses"] == 2
    assert prompt_template_config.execution_settings.extension_data["stop"] == ["\n"]
    assert prompt_template_config.execution_settings.extension_data["logit_bias"] == {"1": 1}


def test_custom_prompt_template_config_from_json():
    prompt_template_json = """
    {
        "schema": 2,
        "type": "completion2",
        "description": "Custom description.",
        "execution_settings": {
            "default": {
                "temperature": 0.5,
                "top_p": 0.5,
                "presence_penalty": 0.5,
                "frequency_penalty": 0.5,
                "max_tokens": 128,
                "number_of_responses": 2,
                "stop": ["s"],
                "logit_bias": {"1": 1}
            }
        }
    }
    """
    prompt_template_config = PromptTemplateConfig[OpenAIChatRequestSettings].from_json(prompt_template_json)
    assert prompt_template_config.schema_ == 2
    assert prompt_template_config.type == "completion2"
    assert prompt_template_config.description == "Custom description."
    assert prompt_template_config.execution_settings.temperature == 0.5
    assert prompt_template_config.execution_settings.top_p == 0.5
    assert prompt_template_config.execution_settings.presence_penalty == 0.5
    assert prompt_template_config.execution_settings.frequency_penalty == 0.5
    assert prompt_template_config.execution_settings.max_tokens == 128
    assert prompt_template_config.execution_settings.number_of_responses == 2
    assert prompt_template_config.execution_settings.stop == ["s"]
    assert prompt_template_config.execution_settings.logit_bias == {"1": 1}


def test_chat_prompt_template():
    chat_prompt_template = ChatPromptTemplate(
        "{{$user_input}}",
        PromptTemplateEngine(),
        prompt_config=PromptTemplateConfig(),
    )

    assert chat_prompt_template.messages == []


def test_chat_prompt_template_with_messages():
    prompt_template_config = PromptTemplateConfig[OpenAIChatRequestSettings].from_execution_settings(
        messages=[{"role": "system", "content": "Custom system prompt."}],
    )
    chat_prompt_template = ChatPromptTemplate[OpenAIChatMessage](
        "{{$user_input}}",
        PromptTemplateEngine(),
        prompt_config=prompt_template_config,
        parse_messages=True,
    )
    print(chat_prompt_template.messages)
    assert len(chat_prompt_template.messages) == 1
    assert chat_prompt_template.messages[0].role == "system"
    assert chat_prompt_template.messages[0].content_template.template == "Custom system prompt."


def test_chat_prompt_template_with_system_prompt():
    prompt_template_config = PromptTemplateConfig[OpenAIChatRequestSettings].from_execution_settings(
        chat_system_prompt="Custom system prompt.",
    )
    chat_prompt_template = ChatPromptTemplate[OpenAIChatMessage](
        "{{$user_input}}",
        PromptTemplateEngine(),
        prompt_config=prompt_template_config,
        parse_chat_system_prompt=True,
    )
    print(chat_prompt_template.messages)
    assert len(chat_prompt_template.messages) == 1
    assert chat_prompt_template.messages[0].role == "system"
    assert chat_prompt_template.messages[0].content_template.template == "Custom system prompt."
