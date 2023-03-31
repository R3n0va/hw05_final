from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test_slug',
            description='Тестовое описание группы',
        )

        cls.user_author = User.objects.create_user(
            username='user_author')
        cls.another_user = User.objects.create_user(
            username='another_user')

        cls.post = Post.objects.create(
            text='Текст который просто больше 15 символов...',
            author=cls.user_author,
            group=cls.group,
        )
        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.another_user)
        cls.post_author = Client()
        cls.post_author.force_login(cls.user_author)
        cls.field_urls_code = {
            reverse(
                'posts:index'): HTTPStatus.OK,
            reverse(
                'posts:group_list',
                kwargs={'slug': cls.group.slug}): HTTPStatus.OK,
            reverse(
                'posts:group_list',
                kwargs={'slug': 'bad_slug'}): HTTPStatus.NOT_FOUND,
            reverse(
                'posts:profile',
                kwargs={'username': cls.user_author}): HTTPStatus.OK,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': cls.post.id}): HTTPStatus.OK,
            reverse(
                'posts:edit',
                kwargs={'post_id': cls.post.id}): HTTPStatus.FOUND,
            reverse(
                'posts:create'): HTTPStatus.OK,
            '/unexisting_page/': HTTPStatus.NOT_FOUND,
        }

    def test_unauthorized_user_urls_status_code(self):
        self.field_urls_code[reverse('posts:create')] = 302
        self.field_urls_code[reverse('posts:edit',
                                     kwargs={'post_id': self.post.id})] = 302
        for url, response_code in self.field_urls_code.items():
            with self.subTest(url=url):
                status_code = self.client.get(url).status_code
                self.assertEqual(status_code, response_code)

    def test_authorized_user_urls_status_code(self):
        self.field_urls_code[reverse('posts:edit',
                                     kwargs={'post_id': self.post.id})] = 302
        for url, response_code in self.field_urls_code.items():
            with self.subTest(url=url):
                status_code = self.authorized_user.get(url).status_code
                self.assertEqual(status_code, response_code)

    def test_author_user_urls_status_code(self):
        self.field_urls_code[reverse('posts:edit',
                                     kwargs={'post_id': self.post.id})] = 200
        for url, response_code in self.field_urls_code.items():
            with self.subTest(url=url):
                status_code = self.post_author.get(url).status_code
                self.assertEqual(status_code, response_code)
