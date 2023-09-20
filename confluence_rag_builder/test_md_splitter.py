import unittest
from .md_splitter import split_markdown_document

class TestSplitMarkdownDocument(unittest.TestCase):
    def test_split_markdown_document(self):
        markdown_content = """# Title 1
## Subtitle 1
Content line 1
Content line 2
## Subtitle 2
Content line 3
# Title 3
Content line 4"""

        # Test depth 1
        expected_output_depth_1 = [
            """# Title 1
## Subtitle 1
Content line 1
Content line 2
## Subtitle 2
Content line 3""",
            """# Title 3
Content line 4""",
        ]

        sections_depth_1 = split_markdown_document(markdown_content, 1)

        # Assert the number of elements in the resulting array
        self.assertEqual(len(sections_depth_1), len(expected_output_depth_1), "Number of elements in the resulting array is different for depth 1")

        # Compare each element in the resulting array
        for i, section in enumerate(sections_depth_1):
            self.assertEqual(section.strip(), expected_output_depth_1[i].strip(), f"Element at index {i} is different for depth 1")

        # Test depth 2
        expected_output_depth_2 = [
            """# Title 1
## Subtitle 1
Content line 1
Content line 2""",
            """# Title 1
## Subtitle 2
Content line 3""",
            """# Title 3
Content line 4""",
        ]

        sections_depth_2 = split_markdown_document(markdown_content, 2)

        # Print the sections to debug
        print("Sections at depth 2:")
        for i, section in enumerate(sections_depth_2):
            print(f"Section {i+1}:\n{section}\n")

        # Assert the number of elements in the resulting array
        self.assertEqual(len(sections_depth_2), len(expected_output_depth_2), "Number of elements in the resulting array is different for depth 2")

        # Compare each element in the resulting array
        for i, section in enumerate(sections_depth_2):
            self.assertEqual(section.strip(), expected_output_depth_2[i].strip(), f"Element at index {i} is different for depth 2")

        print("All Tests Passed!")

if __name__ == "__main__":
    unittest.main()
