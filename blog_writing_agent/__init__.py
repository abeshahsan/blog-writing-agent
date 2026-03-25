__all__ = ["BlogService"]


def __getattr__(name: str):
	if name == "BlogService":
		from .services.blog_service import BlogService

		return BlogService
	raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
