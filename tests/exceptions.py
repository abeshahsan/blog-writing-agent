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
