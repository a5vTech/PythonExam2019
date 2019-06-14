import unittest, os, warnings, glob
#from Main import *
import Main
class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.url = 'https://clbokea.github.io/exam/'
        self.projectDirectory = 'WebCrawled'
        #Fix python ressource warning (Due to bad allocation to python)
        warnings.simplefilter("ignore", ResourceWarning)


    def test_createProjectFolder(self):
        Main.createProjectFolder(self.projectDirectory)
        self.assertTrue(os.path.exists(self.projectDirectory))

    def test_fetchLinks(self):
        self.links = Main.fetchAllLinksFromBasePage(self.projectDirectory, self.url)
        self.assertTrue(self.links)
        self.assertEqual(len(self.links),5)
        
 




if __name__ == "__main__":
    unittest.main()