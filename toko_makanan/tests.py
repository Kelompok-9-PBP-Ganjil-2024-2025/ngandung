from django.test import TestCase, Client
from django.urls import reverse
from toko_makanan.models import RumahMakan, Makanan

class RumahMakanMakananTests(TestCase):
    def setUp(self):
        # Setup rumah makan
        self.rumah_makan = RumahMakan.objects.create(
            kode_provinsi=31,
            nama_provinsi="DKI Jakarta",
            bps_kode_kabupaten_kota=3171,
            bps_nama_kabupaten_kota="Jakarta Selatan",
            nama_rumah_makan="Dallas",
            alamat="Jalan Merdeka No.1",
            latitude=-6.21462,
            longitude=106.84513,
            tahun=2020,
            masakan_dari_mana="Jawa",
            makanan_berat_ringan="Berat",
        )

        # Setup makanan
        self.makanan = Makanan.objects.create(
            name="Nasi Kimpul", price=10000, rumah_makan=self.rumah_makan
        )
        self.client = Client()

    def test_rumah_makan_creation(self):
        self.assertEqual(self.rumah_makan.nama_rumah_makan, "Dallas")
        self.assertEqual(self.rumah_makan.nama_provinsi, "DKI Jakarta")

    def test_show_main_view(self):
        response = self.client.get(reverse("toko_makanan:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mainPage/index.html")
        self.assertContains(response, self.rumah_makan.nama_rumah_makan)

    def test_rumah_makan_by_id_exist(self):
        response = Client().get(
            reverse("toko_makanan:detail_rumah_makan", args=[self.rumah_makan.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_rumah_makan_by_id_without_login(self):
        response = Client().get(
            reverse("toko_makanan:edit_toko", args=[self.rumah_makan.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_rumah_makan_by_id_without_login(self):
        response = Client().get(
            reverse("toko_makanan:delete_toko", args=[self.rumah_makan.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_makanan_creation(self):
        self.assertEqual(self.makanan.name, "Nasi Kimpul")
        self.assertEqual(self.makanan.price, 10000)
        self.assertEqual(self.makanan.rumah_makan, self.rumah_makan)

    def test_add_makanan_without_login(self):
        response = self.client.post(
            reverse("toko_makanan:add_makanan"),
            {"name": "Bakso", "price": 12000, "toko_id": self.rumah_makan.id},
        )
        self.assertEqual(response.status_code, 302)

    def test_edit_makanan_by_id_exist_without_login(self):
        response = Client().get(
            reverse("toko_makanan:edit_makanan", args=[self.makanan.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_makanan_by_id_exist_without_login(self):
        response = Client().get(
            reverse("toko_makanan:delete_makanan", args=[self.makanan.pk])
        )
        self.assertEqual(response.status_code, 302)
