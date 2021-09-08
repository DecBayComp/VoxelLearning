from django.test import TestCase

from fileapp.models import File


class FileTestCase(TestCase):
    def setUp(self):
        File.objects.create(id=1, file="/home/user/toto.txt")
        File.objects.create(id=2, file="/home/user/tata.txt")

    def test_file(self):
        f1 = File.objects.get(id=1)
        f2 = File.objects.get(id=2)
        self.assertEqual(f1.id, 1)
        self.assertEqual(f2.id, 2)
        self.assertEqual(str(f1), '/home/user/toto.txt')
        self.assertEqual(str(f2), '/home/user/tata.txt')
