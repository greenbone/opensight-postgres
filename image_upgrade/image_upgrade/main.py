from docker_hub import DockerHub


def main() -> int:
    d = DockerHub().repository_get_tags("postgres")
    print(d)
    return 0


if __name__ == "__main__":
    main()
