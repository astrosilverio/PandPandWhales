import unittest
import one_sentence_per_line as ospl
import nltk
import os

class Test_Sentences(unittest.TestCase):

    def setUp(self):
    
        self.test_one_line = "This, is just; one sentence.\n"
        with open("test_one_line.txt", 'w') as f:
            f.write(self.test_one_line)
        self.test_multi_lines = "This is just one sentence.\r\nThis is another sentence.\n"
        with open("test_multi_lines.txt", 'w') as f:
            f.write(self.test_multi_lines)
        self.test_multi_para = "This is just one sentence.\r\nThis is another sentence.\r\nThis is the last sentence in this paragraph.\r\n\r\nThis is the first sentence of the second paragraph.\n"
        with open("test_multi_para.txt", 'w') as f:
            f.write(self.test_multi_para)
        
    def test_one_line(self):
        ospl.process_data("test_one_line.txt", "out.txt", True)
        with open("out.txt", 'r') as f:
            f.seek(0)
            output = f.read()
            expected = "This , is just ; one sentence . \n"
            self.assertEqual(expected, output)
            
    def test_multi_lines(self):
        ospl.process_data("test_multi_lines.txt", "out.txt", True)
        with open("out.txt", 'r') as f:
            f.seek(0)
            output = f.read()
            expected = "This is just one sentence . \nThis is another sentence . \n"
            self.assertEqual(expected, output)
            
    def test_multi_para(self):
        ospl.process_data("test_multi_para.txt","out.txt", True)
        with open("out.txt", 'r') as f:
            f.seek(0)
            output = f.read()
            expected = "This is just one sentence . \nThis is another sentence . \nThis is the last sentence in this paragraph . \nThis is the first sentence of the second paragraph . \n"
            self.assertEqual(expected, output)
            
    def tearDown(self):
        os.remove("test_one_line.txt")
        os.remove("test_multi_lines.txt")
        os.remove("test_multi_para.txt")
        os.remove("out.txt")
        
        
if __name__ == "__main__":

    unittest.main()