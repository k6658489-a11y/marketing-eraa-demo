import csv
import pathlib
import tempfile
import unittest
from tools.build import render_page, theme_for, build, read_records

class BuildTests(unittest.TestCase):
    def test_theme_mapping(self):
        self.assertEqual(theme_for("men's bespoke tailoring").key,'tailor')
        self.assertEqual(theme_for('Barber / men\'s grooming').key,'barber')
        self.assertEqual(theme_for('Shoe and leather repair').key,'shoe')
        self.assertEqual(theme_for('Clothing alterations').key,'alterations')
    def test_page_is_unofficial_and_verifiable(self):
        h = render_page({'country':'uk','slug':'test-shop','business_name':'Sample & Co','city':'London','industry':'Tailoring','services':'Alterations; Fitting','headline':'Example concept'})
        self.assertIn('data-demo-key="uk/test-shop"', h)
        self.assertIn('UNOFFICIAL CONCEPT PREVIEW', h)
        self.assertIn('noindex,nofollow,noarchive', h)
        self.assertNotIn('<form', h)
        self.assertIn('Sample &amp; Co', h)
    def test_rejects_unsafe_slugs(self):
        with tempfile.TemporaryDirectory() as d:
            csv_file=pathlib.Path(d)/'leads.csv'
            csv_file.write_text('country,business_name,slug,industry,city,services,approved_for_demo\nuk,Demo,../private,tailor,London,A,yes\n')
            with self.assertRaises(ValueError):read_records(csv_file)
    def test_build_only_approved(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d)
            inp=root/'data.csv'
            inp.write_text('country,business_name,slug,industry,city,services,approved_for_demo\nusa,Example,example,cleaning,Denver,Home Cleaning,yes\nuk,Other,other,cleaning,London,Cleaning,no\n')
            out=build(root,inp)
            self.assertEqual(len(out),1)
            self.assertTrue((root/'usa'/'example'/'index.html').exists())
            self.assertFalse((root/'uk'/'other'/'index.html').exists())

if __name__=='__main__':unittest.main()
