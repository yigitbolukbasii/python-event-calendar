		onPressKeyDict[app.DIK_F4]	= lambda : self.__PressQuickSlot(7)
#altına ekle
		onPressKeyDict[app.DIK_F8]	= lambda : self.OpenTimerWindow()


#en alta ekle
	def OpenTimerWindow(self):
		self.interface.OpenTimerWindow()