# on line 3, replace tfidf with the name of your script, minus the .py extension

from tfidf import TfidfCalculator

from collections import Counter
from pathlib import Path
from pytest import approx

def test_init():
    """ Test the TfidfCalculator.__init__() method. """
    # instantiate class
    calc = TfidfCalculator()
    
    # were the tf and df attributes created?
    assert hasattr(calc, "tf"), \
        "instance of TfidfCalculator has no tf attribute"
    assert hasattr(calc, "df"), \
        "instance of TfidfCalculator has no df attribute"
    
    # are there any attributes or methods we weren't expecting?
    attributes = {attr for attr in dir(calc) if attr[0:2] != "__"}
    unexpected = attributes - {"tf", "df", "read_file", "important_words"}
    assert len(unexpected) == 0,\
        ("after running __init__(), TfidfCalculator instance has the following"
         f" unexpected attributes or methods: {unexpected}")
    
    # are tf and df the correct data types?
    assert isinstance(calc.tf, dict), \
        "tf attribute of TfidfCalculator instance should be a dictionary"
    assert isinstance(calc.df, Counter), \
        ("tf attribute of TfidfCalculator instance should be an instance of"
         " collections.Counter")
    
    # are tf and df empty?
    assert len(calc.tf) == 0, \
        "tf attribute of TfidfCalculator should initially be empty"
    assert len(calc.df) == 0, \
        "df attribute of TfidfCalculator should initially be empty"


def test_read_file():
    """ Test the TfidfCalculator.read_file() method.
    
    Side effects:
        Creates and deletes two temporary files called TEMP_TEXT_FILE1
        and TEMP_TEXT_FILE2.
    """
    # instantiate class
    calc = TfidfCalculator()
    
    # create temporary files
    path = Path("TEMP_TEXT_FILE1")
    path2 = Path("TEMP_TEXT_FILE2")
    path.write_text("This is a test. This is only a test.")
    path2.write_text("This, too, is just a test.")
    
    # use try/except to ensure we clean up the temporary files even if
    # something goes wrong
    try:
        # read first file
        calc.read_file(str(path))
        
        # after reading one file, did the tf attribute get modified properly?
        assert str(path) in calc.tf, \
            "read_file() did not add the filename as a key of tf"
        assert isinstance(calc.tf[str(path)], Counter), \
            ("read_file() should have added a Counter object as the value of"
             f" tf[filename], but it added a {type(calc.tf[str(path)])} object"
             " instead")
        assert "only" in calc.tf[str(path)], \
            ("after read_file() reads a file, tf[filename] should contain"
             "the words in that file as keys")

        # after reading one file, did the words of the file get counted
        # correctly in tf?
        assert calc.tf[str(path)]["only"] == 1, \
            ("after read_file() reads a file, tf[filename] should contain"
             "counts of the words in that file")
        assert calc.tf[str(path)]["test"] == 2, \
            ("after read_file() reads a file, tf[filename] should contain"
             "counts of the words in that file")
        assert len(calc.tf[str(path)]) == 5, \
            ("after read_file() reads a file, tf[filename] should contain"
             "counts for each unique word in the file")
        assert max(calc.tf[str(path)].values()) == 2, \
            ("after read_file() read one file, some words in tf[filename]"
             " have a higher count than expected")
        assert min(calc.tf[str(path)].values()) == 1, \
            ("after read_file() read one file, some words in tf[filename]"
             " have a lower count than expected")
        
        # after reading one file, did the df attribute get modified properly?
        assert "only" in calc.df, \
            ("after read_file() reads a file, df should contain the words in"
             " that file as keys")
        assert calc.df["only"], \
            ("after read_file() reads a file, each word in the file should be"
             " present as a key in df")
        
        # after reading one file, did the words of the file get counted
        # correctly in df?
        assert calc.df["only"] == 1, \
            ("after read_file() reads a file, the value of df[word] should"
             " increase by 1 for each unique word in the file")
        assert calc.df["test"] == 1, \
            ("df should reflect the number of documents that contain a"
             " particular ")
        assert len(calc.df) == 5, \
            ("after read_file() reads a file, df should contain counts of the"
             " words in that file")
        assert max(calc.df.values()) == 1, \
            ("after read_file() has read one file, all keys in df should have a"
             " count of 1")
        assert min(calc.df.values()) == 1, \
            ("after read_file() has read one file, all keys in df should have a"
             " count of 1")
        
        # read second file
        calc.read_file(str(path2))
        
        # after reading two files, did the tf attribute get modified properly?
        assert str(path) in calc.tf, \
            ("when read_file() reads a second file, tf should retain the"
             " information from the first file")
        assert str(path2) in calc.tf, \
            ("when read_file() reads a second file, tf should contain"
             " information from both files")
        assert len(calc.tf) == 2, \
            ("after read_file() has read two files, tf should contain"
             " exactly two keys (one for each file)")
            
        # after reading two files, did the words in the second file get
        # counted properly?
        assert len(calc.tf[str(path2)]) == 6, \
            ("after reading a second file with read_file(), tf[filename]"
             " does not contain the correct number of items")
        
        # after reading two files, did the df attribute get modified properly?
        # did the words in the two files get counted properly?
        assert "only" in calc.df, \
            ("after reading a second file, words from the first file are no"
             " longer in df")
        assert "just" in calc.df, \
            ("after reading a second file, words from the second file are not"
             " in df")
        assert set(calc.df) == {"this", "is", "a", "test", "only", "too",
                                "just"}, \
            ("df contains the wrong set of keys after reading two files")
        assert calc.df["only"] == 1, \
            ("after reading a second file, words from the first file have an"
             " unexpected count in df")
        assert calc.df["just"] == 1, \
            ("after reading a second file, words from the second file have an"
             " unexpected count in df")
        assert calc.df["test"] == 2, \
            ("after reading a second file, words that appear in both files"
             " should have a count of 2 in df")
        assert min(calc.df.values()) == 1, \
            ("after read_file() has read a second file, no key in df should"
             " have a value less than 1")
        assert max(calc.df.values()) == 2, \
            ("after read_file() has read a second file, no key in df should"
             " have a value greater than 2")

        # are there any attributes (or methods) we weren't expecting?
        attributes = {attr for attr in dir(calc) if attr[0:2] != "__"}
        unexpected = attributes - {"tf", "df", "read_file", "important_words"}
        assert len(unexpected) == 0,\
            ("after running read_file(), TfidfCalculator has the following"
             f" unexpected attributes or methods: {unexpected}")

    finally:
        # try to delete files
        for p in [path, path2]:
            try:
                p.unlink(missing_ok=True)
            except:
                print(f"unable to delete temporary file {p.name}")


def test_important_words():
    """ Test the TfidfCalculator.important_words() method.
    
    Side effects:
        Creates and deletes a temporary directory called TEMP_CORPUS_DIR.
        Creates and deletes a number of temporary files inside TEMP_CORPUS_DIR.
    """
    # create and populate temporary directory
    temp_dir = Path("TEMP_CORPUS_DIR")
    path1 = temp_dir / "FILE1"
    path2 = temp_dir / "FILE2"
    path3 = temp_dir / "FILE3"
    path4 = temp_dir / "FILE4"
    paths = [path1, path2, path3, path4]
    texts = [("a a a a a a a a a a a a a a a a a a a a "
              "b b b b b b b b b b b b b b b b b b b "
              "c c c c c c c c c c c c c c c c c c "
              "d d d d d d d d d d d d d d d d d "
              "e e e e e e e e e e e e e e e e "
              "f f f f f f f f f f f f f f f "
              "g g g g g g g g g g g g g g "
              "h h h h h h h h h h h h h "
              "i i i i i i i i i i i i "
              "j j j j j j j j j j j "
              "k k k k k k k k k k "
              "l l l l l l l l l "
              "m m m m m m m m "),
             ("a a a a a a a a a a "
              "c c c c c c c c c "
              "e e e e e e e e e "
              "g g g g g g g g "
              "i i i i i i i "
              "k k k k k k "
              "m m m m m "
              "o o o o "
              "q q q "
              "s s "),
             ("a "
              "d d "
              "g g g "
              "j j j j "
              "m m m m m "
              "p p p p p p "
              "s s s s s s s "
              "v v v v v v v v "
              "y y y y y y y y y "
              "1 1 1 1 1 1 1 1 1 1"),
             ("a "
              "e e "
              "i i i "
              "m m m m "
              "q q q q q "
              "u u u u u u "
              "y y y y y y y "
              "2 2 2 2 2 2 2 2 ")]
    
    # use try/except to create directory and files so we can delete them even if
    # something goes wrong
    try:
        # create TfidfCalculator, directory, files
        calc = TfidfCalculator()
        temp_dir.mkdir()
        for path, text in zip(paths, texts):
            path.write_text(text, encoding="utf-8")
            calc.read_file(str(path))
        
        # test important_words with default value of num_words
        try:
            important1 = calc.important_words(str(path1))
        except TypeError:
            raise AssertionError("important_words() should have one required"
                                 " parameter (filename) and one optional"
                                 " parameter (num_words) with a default value"
                                 " of 10")
        assert len(important1) == 10, \
            ("important_words() should return a dict of length 10 by default")
        
        # check one tf-idf value early in the test suite so we can give specific
        # feedback if the calculation is incorrect
        if "d" in important1:
            assert important1["d"] == approx(0.064744516865489), \
                "important_words() calculates tf-idf incorrectly"
        
        # check the set of keys that were returned
        expected_keys = ["b", "f", "h", "c", "l", "d", "j", "k", "e", "g"]
        actual_keys = list(important1.keys())
        missing_keys = set(expected_keys) - set(actual_keys)
        unexpected_keys = set(actual_keys) - set(expected_keys)
        unexpected_msgs = []
        if missing_keys:
            unexpected_msgs.append(
                "the dictionary returned by important_words() failed to"
                f" return the following keys: {missing_keys}"
            )
        if unexpected_keys:
            unexpected_msgs.append(
                "the dictionary returned by important_words() contained the"
                f" following unexpected keys: {unexpected_keys}"
            )
        if unexpected_msgs:
            hints = ("(did you sort words in descending order of tf-idf scores?"
                     " did you calculate tf-idf correctly?")
            raise AssertionError("; ".join(unexpected_msgs))
        
        # check the order of keys that were returned
        assert actual_keys == expected_keys, \
            ("the keys in the dictionary returned by important_words() are in"
             " an unexpected order")
        
        # check the full set of expected tf-idf calculations
        expected1 = {"b": 0.144723037699329,
                     "f": 0.114255029762628,
                     "h": 0.099021025794278,
                     "c": 0.068553017857577,
                     "l": 0.068553017857577,
                     "d": 0.064744516865489,
                     "j": 0.041893510912964,
                     "k": 0.038085009920876,
                     "e": 0.025290731644113,
                     "g": 0.022129390188599}
        assert important1 == approx(expected1), \
            "important_words() calculates tf-idf incorrectly"
        
        # make sure important_words() honors num_words when specified
        important2 = calc.important_words(str(path2), num_words=5)
        assert len(important2) == 5, \
            ("important_words() should return the number of words specified by"
             " the num_words parameter")
        
        # make sure important_words() does the right thing when
        # num_words is None
        important3 = calc.important_words(str(path1), num_words=None)
        assert len(important3) == 13, \
            ("important_words() should return all words in the document if"
             " num_words is None")
        
        # make sure no additional attributes were set by important_words()
        attributes = {attr for attr in dir(calc) if attr[0:2] != "__"}
        unexpected = attributes - {"tf", "df", "read_file", "important_words"}
        assert len(unexpected) == 0, \
            ("after running important_words(), TfidfCalculator has the following"
             f" unexpected attributes or methods: {unexpected}")
        
    finally:
        # clean up files and directories
        for p in paths:
            try:
                p.unlink(missing_ok=True)
            except:
                print(f"unable to delete temporary file {str(p)}")
        try:
            temp_dir.rmdir()
        except:
            print(f"unable to delete temporary directory {str(temp_dir)}")
