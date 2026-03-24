from blog_writing_agent import BlogService


def main() -> None:
	service = BlogService()
	result = service.generate_blog("Write a blog on Self Attention")
	print(result["final"])


if __name__ == "__main__":
	main()