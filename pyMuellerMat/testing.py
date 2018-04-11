import common_mms as mms


verbose=True


p1 = mms.Polarizer()
p2 = mms.HorizontalPolarizer()
p3 = mms.VerticalPolarizer()
p4 = mms.WollastonPrism()
p5 = mms.Retarder()
p6 = mms.HWP()
p7 = mms.QWP()
p8 = mms.Rotator()

if verbose:
	print(p1.evaluate())
	print(p2.evaluate())
	print(p3.evaluate())
	print(p4.evaluate())
	print(p5.evaluate())
	print(p6.evaluate())
	print(p7.evaluate())
	print(p8.evaluate())
else:
	t = p1.evaluate()
	t = p2.evaluate()
	t = p3.evaluate()
	t = p4.evaluate()
	t = p5.evaluate()
	t = p6.evaluate()
	t = p7.evaluate()
	t = p8.evaluate()
