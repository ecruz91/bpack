def as_myp(self):		
	return self._html_output(
	normal_row = '<div class="col-sm-6"><label%(html_class_attr)s>%(label)s</label> %(field)s%(help_text)s %(errors)s</p></div>',
	row_ender = '</p>',
	error_row = '%s',
	help_text_html = ' <span class="helptext">%s</span>',
	errors_on_separate_row = False)

def as_myp2(self):		
	return self._html_output(
	normal_row = '<div class="col-sm-12"><label%(html_class_attr)s>%(label)s</label> %(field)s%(help_text)s %(errors)s</p></div>',
	row_ender = '</p>',
	error_row = '%s',
	help_text_html = ' <span class="helptext">%s</span>',
	errors_on_separate_row = False)