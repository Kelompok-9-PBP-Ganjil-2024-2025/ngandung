from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import RumahMakan, Rating
from .forms import RatingForm
import json


class RumahMakanModelTest(TestCase):
    def setUp(self):
        self.rumah_makan = RumahMakan.objects.create(
            kode_provinsi=1,
            nama_provinsi="Provinsi A",
            bps_kode_kabupaten_kota=101,
            bps_nama_kabupaten_kota="Kota A",
            nama_rumah_makan="Rumah Makan A",
            alamat="Alamat A",
            latitude=1.234567,
            longitude=2.345678,
            tahun=2021,
            masakan_dari_mana="Masakan A",
            makanan_berat_ringan="Berat",
            average_rating=0.0,
            number_of_ratings=0,
        )

    def test_rumah_makan_creation(self):
        self.assertEqual(self.rumah_makan.nama_rumah_makan, "Rumah Makan A")
        self.assertEqual(str(self.rumah_makan), "Rumah Makan A")


class RatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.rumah_makan = RumahMakan.objects.create(
            kode_provinsi=2,
            nama_provinsi="Provinsi B",
            bps_kode_kabupaten_kota=202,
            bps_nama_kabupaten_kota="Kota B",
            nama_rumah_makan="Rumah Makan B",
            alamat="Alamat B",
            latitude=3.456789,
            longitude=4.567890,
            tahun=2022,
            masakan_dari_mana="Masakan B",
            makanan_berat_ringan="Ringan",
            average_rating=0.0,
            number_of_ratings=0,
        )
        self.rating = Rating.objects.create(
            user=self.user,
            rumah_makan=self.rumah_makan,
            rating=5,
            review="Excellent food!",
        )

    def test_rating_creation(self):
        self.assertEqual(self.rating.rating, 5)
        self.assertEqual(self.rating.review, "Excellent food!")
        self.assertEqual(self.rating.user.username, "testuser")
        self.assertEqual(self.rating.rumah_makan.nama_rumah_makan, "Rumah Makan B")


class RatingFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "rating": 4,
            "review": "Great place!",
        }
        form = RatingForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "rating": 6,  # Invalid rating (should be between 1 and 5)
            "review": "Awesome!",
        }
        form = RatingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="viewuser", password="password123"
        )
        self.rumah_makan = RumahMakan.objects.create(
            kode_provinsi=3,
            nama_provinsi="Provinsi C",
            bps_kode_kabupaten_kota=303,
            bps_nama_kabupaten_kota="Kota C",
            nama_rumah_makan="Rumah Makan C",
            alamat="Alamat C",
            latitude=5.678901,
            longitude=6.789012,
            tahun=2023,
            masakan_dari_mana="Masakan C",
            makanan_berat_ringan="Berat",
            average_rating=0.0,
            number_of_ratings=0,
        )

    def test_get_all_toko_page(self):
        response = self.client.get(reverse("rating_toko:get_all_toko_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "toko.html")

    def test_get_all_toko(self):
        response = self.client.get(reverse("rating_toko:get_all_toko"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 101)
        self.assertEqual(data[0]["fields"]["nama_rumah_makan"], "BREW & CHEW")

    def test_get_toko(self):
        response = self.client.get(
            reverse("rating_toko:get_toko", args=[self.rumah_makan.id])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]["fields"]["nama_rumah_makan"], "Rumah Makan C")

    def test_get_all_ratings_page(self):
        response = self.client.get(
            reverse("rating_toko:get_all_ratings_page", args=[self.rumah_makan.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "toko_specific.html")

    def test_add_rating_not_logged_in(self):
        response = self.client.post(
            reverse("rating_toko:add_rating"),
            {
                "rating": 5,
                "review": "Delicious!",
                "id_rumah_makan": self.rumah_makan.id,
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_add_rating_logged_in(self):
        self.client.login(username="viewuser", password="password123")
        response = self.client.post(
            reverse("rating_toko:add_rating"),
            {
                "rating": 5,
                "review": "Delicious!",
                "id_rumah_makan": self.rumah_makan.id,
            },
        )
        self.assertEqual(response.status_code, 201)
        ratings = Rating.objects.filter(rumah_makan=self.rumah_makan)
        self.assertEqual(ratings.count(), 1)
        self.assertEqual(ratings.first().review, "Delicious!")

    def test_edit_rating(self):
        self.client.login(username="viewuser", password="password123")
        rating = Rating.objects.create(
            user=self.user,
            rumah_makan=self.rumah_makan,
            rating=3,
            review="Good",
        )
        response = self.client.post(
            reverse("rating_toko:edit_rating", args=[rating.id, self.rumah_makan.id]),
            {
                "rating": 4,
                "review": "Very Good",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after edit
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 4)
        self.assertEqual(rating.review, "Very Good")

    def test_delete_rating(self):
        self.client.login(username="viewuser", password="password123")
        rating = Rating.objects.create(
            user=self.user,
            rumah_makan=self.rumah_makan,
            rating=2,
            review="Not great",
        )
        response = self.client.post(
            reverse("rating_toko:delete_rating", args=[rating.id, self.rumah_makan.id])
        )
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Rating.objects.filter(id=rating.id).exists())

    def test_get_user(self):
        response = self.client.get(reverse("rating_toko:get_user", args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]["fields"]["username"], "viewuser")
