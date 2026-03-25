from pathlib import Path

from blog_writing_agent.io import markdown_writer


def test_make_output_filename():
    assert markdown_writer.make_output_filename("Hello World") == "hello_world.md"


def test_make_output_filename_sanitizes_windows_invalid_characters():
    title = 'Understanding Self-Attention: The Core of Modern NLP?*'
    assert (
        markdown_writer.make_output_filename(title)
        == "understanding_self-attention_the_core_of_modern_nlp.md"
    )


def test_make_output_filename_falls_back_when_title_is_symbols_only():
    assert markdown_writer.make_output_filename('::""***|||') == "untitled.md"


def test_write_markdown_output_writes_file(tmp_path, monkeypatch):
    monkeypatch.setattr(markdown_writer, "PROJECT_ROOT", Path(tmp_path))

    file_path = markdown_writer.write_markdown_output("post.md", "# Title\n")

    output_file = Path(file_path)
    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8") == "# Title\n"
