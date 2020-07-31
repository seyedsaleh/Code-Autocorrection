class Setting:
    def __init__(self):
        # grading setting
        self.file_names = []
        self.img_tests = []
        self.beauty_coefficient = 25
        self.report_coefficient = 5
        self.test_1_number = -1
        self.test_2_number = -1
        self.test_1_point = -1
        self.test_2_point = -1
        # output setting
        self.pdf_output = -1
        self.excel_output = -1
        self.grade_output = -1
        self.mos_output = -1
        self.grade_mos_output = -1
        self.similarity_limit = -1
        self.python_python = 1  # default is Docker.
        # advance setting
        self.build_keyWord = 'Successfully built'
        self.cppTest_keyWord = '<<<success>>>'
        self.pyTest_keyWord = 'Failure'
        self.minus_keyWord = 'minus'

    def set_to_none(self):
        self.beauty_coefficient = -1
        self.report_coefficient = -1
        self.test_1_number = -1
        self.test_2_number = -1
        self.test_1_point = -1
        self.test_2_point = -1
        self.file_names = []
        self.img_tests = []

        self.pdf_output = -1
        self.python_python = 1
        self.excel_output = -1
        self.grade_output = -1
        self.mos_output = -1  # default is Docker.
        self.grade_mos_output = -1
        self.similarity_limit = -1

        self.build_keyWord = 'Successfully built'
        self.cppTest_keyWord = '<<<success>>>'
        self.pyTest_keyWord = 'Failure'
        self.minus_keyWord = 'minus'

    def show(self):
        print("___ Setting Parameters:")
        print("beauty_coefficient: ", self.beauty_coefficient)
        print("report_coefficient: ", self.report_coefficient)
        print("test_1_number: ", self.test_1_number, "  test_1_point: ", self.test_1_point)
        print("test_2_number: ", self.test_2_number, "  test_2_point: ", self.test_2_point)
        print("pdf_output: ", self.pdf_output, "  excel_output: ", self.excel_output)
        print("python python: ",self.python_python)
        print("grade_output: ", self.grade_output, "  mos_output: ", self.mos_output)
        print("grade_mos_output: ", self.grade_mos_output, "  similarity_limit: ", self.similarity_limit)
        print("file_names: ", self.file_names)
        print("img_tests: ", self.img_tests)
        print("key words: ", self.build_keyWord, ' ', self.cppTest_keyWord, ' ',  self.minus_keyWord, ' ', self.pyTest_keyWord)


