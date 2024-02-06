import httpx
from model import DockerTagsPage, DockerTagsResult


class DockerHubResponseError(Exception):
    """DockerHub class response base exception"""


class DockerHub(httpx.Client):
    def __init__(
        self,
        user: str = None,
        password: str = None,
        timeout: int = 10,
        default_namespace: str = "library",
        default_page_size: int = 100,
    ):
        super().__init__(base_url="https://hub.docker.com/v2", timeout=timeout)
        self.namespace = default_namespace
        self.page_size = default_page_size
        if user and password:
            self._login(user, password)

    @property
    def get_default_namespace() -> str:
        return self.default_namespace

    def _get_data_as_dict(self, url: str) -> dict:
        res = self.get(url)
        res.raise_for_status()
        return res.json()

    def _login(self, user: str, password: str) -> None:
        pass

    def repository_get_tags_by_page(
        self,
        repository: str,
        namespace: str = None,
        page: int = 1,
        page_size: int = None,
    ) -> dict:
        if not namespace:
            namespace = self.namespace
        if not page_size:
            page_size = self.page_size
        url = f"/namespaces/{namespace}/repositories/{repository}/tags?page={page}&page_size={page_size}"
        return DockerTagsPage(**self._get_data_as_dict(url))

    def repository_get_tags(self, repository: str, namespace: str = None):
        dcl: list[DockerTagsResult] = []
        dc: DockerTagsPage = self.repository_get_tags_by_page(repository, namespace = namespace)
        dcl.extend(dc.results)
        while dc.next != None:
            print(dc.next)
            dc = DockerTagsPage(**self._get_data_as_dict(dc.next))
            dcl.extend(dc.results)
        return dcl


