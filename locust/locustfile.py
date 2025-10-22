from locust import HttpUser, task, between

class WordpressLoadTest(HttpUser):
    

    @task(3)
    def post_imagem_grande(self):
        """Cenário A: Post com imagem ~890KB"""
        self.client.get("/index.php/2025/10/21/imagem-890kb/")

    @task(2)
    def post_imagem_media(self):
        """Cenário B: Post com imagem ~440KB"""
        self.client.get("/index.php/2025/10/21/imagem-440kb/")

    @task(1)
    def post_texto(self):
        """Cenário C: Post com texto ~300KB"""
        self.client.get("/index.php/2025/10/21/texto-300kb/")


# http://localhost/index.php/2025/10/21/imagem-440kb/
# http://localhost/index.php/2025/10/21/imagem-890kb/
# http://localhost/index.php/2025/10/21/texto-300kb/