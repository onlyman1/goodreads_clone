from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from books.models import Book
from users.models import CustomUser


class BookTestCase(TestCase):
    def test_list_books(self):
        response = self.client.get(reverse('list'))
        self.assertContains(response, 'There is no books')

    def test_list_page(self):
        Book.objects.create(title='Book1', description='haqida1', isbn='12-s-4')
        Book.objects.create(title='Book2', description='haqida2', isbn='13-d-6')
        Book.objects.create(title='Book3', description='haqida3', isbn='14-g-7')

        books = Book.objects.all()
        response = self.client.get(reverse('list'))


        for i in books:
            self.assertContains(response, i.title.upper())

    def test_detail_page(self):
        book = Book.objects.create(title='Book1', description='haqida1', isbn='12-s-4')

        response = self.client.get(reverse('detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title.upper())
        self.assertContains(response, book.description)
        self.assertContains(response, book.isbn)

    def test_book_search(self):
        book1 = Book.objects.create(title='Gerakl and', description='hello world')
        book2 = Book.objects.create(title='Bruce Lee', description='hello lee')
        book3 = Book.objects.create(title='Fly gerakl', description='hello fly')

        response = self.client.get(reverse('list')+'?q=gerakl')

        self.assertContains(response, book1.title.upper())
        self.assertNotContains(response, book2.title.upper())
        self.assertContains(response, book3.title.upper())

        response = self.client.get(reverse('list') + '?q=bruce')

        self.assertContains(response, book2.title.upper())
        self.assertNotContains(response, book1.title.upper())
        self.assertNotContains(response, book3.title.upper())

        response = self.client.get(reverse('list') + '?q=fly')

        self.assertContains(response, book3.title.upper())
        self.assertNotContains(response, book2.title.upper())
        self.assertNotContains(response, book1.title.upper())



class BookReviewTestCase(TestCase):
    def test_review(self):
        book = Book.objects.create(title='You and Me', description='Good book')

        user = CustomUser.objects.create(username='hunter005', first_name='Erik',
                                         last_name='christ', email='christ@gmail.com',)
        user.set_password('11223344')
        user.save()

        self.client.login(username='hunter005', password='11223344')

        self.client.post(reverse('review', kwargs={'id': book.id}),
                         data={
                             'star_given': '4',
                             'review_text': 'Good book'
                         })
        review_new = book.review_set.all()


        self.assertEqual(review_new.count(), 1)
        self.assertEqual(review_new[0].star_given, 4)
        self.assertEqual(review_new[0].review_text, 'Good book')
        self.assertEqual(review_new[0].book_id, book)
        self.assertEqual(review_new[0].user_id, user)





















































