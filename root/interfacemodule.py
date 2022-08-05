import uitimerwindow
#importlara ekle

	def __MakeCubeWindow(self):
		self.wndCube = uiCube.CubeWindow()
		self.wndCube.LoadWindow()
		self.wndCube.Hide()
#altına ekle
	def __MakeTimerWindow(self):
		self.wndTimer = uitimerwindow.TimerWindow()
		self.wndTimer.LoadWindow()


		self.__MakeItemSelectWindow()
#altına ekle
		self.__MakeTimerWindow()


		self.privateShopBuilder.SetItemToolTip(self.tooltipItem
#altına ekle
		self.wndTimer.SetToolTip(self.tooltipItem)


		if self.wndGameButton:
			self.wndGameButton.Destroy()
#altına ekle
		if self.wndTimer:
			self.wndTimer.Destroy()


		del self.wndItemSelect
#altına ekle
		del self.wndTimer

if __name__ == "__main__":
#üstüne ekle
	def OpenTimerWindow(self):
		self.wndTimer.Open()


