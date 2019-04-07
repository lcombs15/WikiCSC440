from wiki.core import wikireference
import unittest

class TestWikiReference(unittest.TestCase):

    def testIndexing(self):
        text = "text ~[reference1]~ text ~[reference2]~"
        text = wikireference(text)
        self.assertTrue("<small>[1]</small>" in text)

    def testMultipleIndexing(self):
        text = "text ~[reference1]~ text ~[reference2]~"
        text = wikireference(text)
        self.assertTrue("<small>[1]</small>" in text and "<small>[2]</small>" in text)

    def testReferenceSectionExists(self):
        text = "~[footnote]~"
        text = wikireference(text)
        self.assertTrue("<h4>References</h4>" in text)

    def testReferenceGenerated(self):
        text = "some text ~[reference]~"
        text = wikireference(text)
        print(text)
        self.assertTrue("1. reference" in text)


if __name__ == '__main__':
    unittest.main()