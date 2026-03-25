from blog_writing_agent.exceptions import (
    BaseException,
    ConfigurationException,
    GraphExecutionException,
    InvalidModelConfigurationException,
    LLMException,
    LLMInvocationException,
    LLMRateLimitException,
    MissingAPIKeyException,
    OutputWriteException,
    PlanGenerationException,
    SectionGenerationException,
)


def test_base_exception_string_and_repr():
    err = BaseException("base failure")
    assert str(err) == "BaseException: base failure"
    assert repr(err) == "BaseException('base failure')"


def test_base_exception_extracts_provider_details_from_validation_payload():
    message = (
        "Response validation failed: 5 validation errors for Unmarshaller\n"
        "body.id\n"
        "  Field required [type=missing, "
        "input_value={'error': {'message': 'Provider returned error', 'code': 502}}, "
        "input_type=dict]"
    )

    err = BaseException(message)

    assert err.details["provider_code"] == 502
    assert err.details["provider_message"] == "Provider returned error"
    assert err.details["validation_error_count"] == 5
    assert err.details["validation_target"] == "Unmarshaller"
    assert "provider_code: 502" in str(err)
    assert "provider_message: Provider returned error" in str(err)


def test_llm_invocation_exception_inheritance():
    err = LLMInvocationException("invoke failed")
    assert isinstance(err, LLMException)
    assert str(err) == "invoke failed"


def test_graph_execution_exception_inheritance():
    err = GraphExecutionException("graph failed")
    assert isinstance(err, BaseException)
    assert str(err) == "GraphExecutionException: graph failed"


def test_configuration_exception_hierarchy():
    err = MissingAPIKeyException("missing key")
    assert isinstance(err, ConfigurationException)
    assert isinstance(err, BaseException)
    assert str(err) == "MissingAPIKeyException: missing key"


def test_invalid_model_configuration_exception():
    err = InvalidModelConfigurationException("invalid model")
    assert isinstance(err, ConfigurationException)
    assert str(err) == "InvalidModelConfigurationException: invalid model"


def test_llm_rate_limit_exception():
    err = LLMRateLimitException("rate limit")
    assert isinstance(err, LLMException)
    assert str(err) == "rate limit"


def test_plan_and_section_generation_exceptions():
    plan_err = PlanGenerationException("plan parse failed")
    section_err = SectionGenerationException("section failed")

    assert isinstance(plan_err, BaseException)
    assert isinstance(section_err, BaseException)
    assert str(plan_err) == "PlanGenerationException: plan parse failed"
    assert str(section_err) == "SectionGenerationException: section failed"


def test_output_write_exception():
    err = OutputWriteException("could not write output")
    assert isinstance(err, BaseException)
    assert str(err) == "OutputWriteException: could not write output"
