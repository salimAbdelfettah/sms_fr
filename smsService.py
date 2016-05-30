#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
import selenium
import urllib, re, time

__all__ = ['BTSMS']

class SMS():
	XPATH = 0
	LINK_TEXT = 1

class BTSMS():
	LINK = "https://www.mon-compte.bouyguestelecom.fr/cas/login"
	GOOD_CONNEXTION_TITLE = "Bouygues Telecom - Espace Client"
	GOOD_SEND_MESSAGE_TITLE = "Bouygues Telecom - Envoyer un SMS"
	
	
	def __init__(self, mail, password):
		print "---------+---------+---------+---------+---------+---------"
		print "Initializing ..."
		#driver = webdriver.Firefox()
		driver = webdriver.PhantomJS()
		self.driver = driver
		driver.set_window_size(1300, 760)
		driver.set_window_position(0, 0)
		driver.get(BTSMS.LINK)
		text_area = driver.find_element_by_id('username')
		text_area.send_keys(mail)
		text_area = driver.find_element_by_id('password')
		text_area.send_keys(password)
		print "Initialization                                         [OK]"
		print "---------+---------+---------+---------+---------+---------"
		print "Connection to the account ..."
		submit_button = driver.find_element_by_id('bt_valider')
		submit_button.click()
		if driver.title == BTSMS.GOOD_CONNEXTION_TITLE:
			print "Connection                                             [OK]"
			print "---------+---------+---------+---------+---------+---------"
			self.canSendMessage = True
			print "Looking for scripts ..."
			scripts = driver.find_elements_by_tag_name("script")
			srcScripts = []
			for script in scripts:
				srcScripts.append(script.get_attribute("src"))
			print "Scripts (1)                                            [OK]"
			print "---------+---------+---------+---------+---------+---------"
			links = driver.find_elements_by_tag_name("a")
			print "Executing scripts ..."
			for script in srcScripts:
				scriptContent = urllib.urlopen(script).read().replace('\xe9', '').replace('\xe0', '').replace('\xa4', '')
				driver.execute_script(scriptContent)
			print "Scripts (2)                                            [OK]"
			print "---------+---------+---------+---------+---------+---------"
			print "Clicking ..."
			#self.click(SMS.XPATH, "//span[@class='guidedTourOverlay']", 5, 0.001)
			self.click(SMS.LINK_TEXT, "Offre", 100, 0.001)
			self.click(SMS.XPATH, "//li[@data-xiti-link='detailForfait_sms']", 100, 0.01)
			self.click(SMS.LINK_TEXT, "Envoyer des SMS depuis mon Espace Client", 100, 0.01)
			self.click(SMS.LINK_TEXT, "Envoyer des SMS depuis mon Espace Client", 100, 0.01)
			handles = driver.window_handles
			driver.switch_to_window(handles.pop())
			time.sleep(2)
			while driver.title != BTSMS.GOOD_SEND_MESSAGE_TITLE :
				time.sleep(1)
				driver.refresh()
			print "Clicking                                               [OK]"
		else:
			this.canSendMessage = False
			print "Connection                                         [NOT OK]"
			print "Wrong username or password !"
		print "---------+---------+---------+---------+---------+---------"
		
	def click(self, how, value, numberOfTicket, sleepTime):
		if numberOfTicket != 0:
			try:
				if how == SMS.XPATH:
					button = self.driver.find_element_by_xpath(value)
				elif how == SMS.LINK_TEXT:
					button = self.driver.find_element_by_link_text(value)
				button.click()
			except selenium.common.exceptions.NoSuchElementException:
				time.sleep(sleepTime)
				self.click(how, value, numberOfTicket - 1, sleepTime)
				
	def sendAnSMS(self, to, text):
		print "---------+---------+---------+---------+---------+---------"
		if self.canSendMessage == True:
			print "Sending message to:", to
			driver = self.driver
			phoneNumber = driver.find_element_by_name("fieldMsisdn")
			message = driver.find_element_by_name("fieldMessage")
			submit = driver.find_element_by_name("Verif")
			phoneNumber.send_keys(to)
			message.send_keys(text)
			submit.click()
			self.click(SMS.XPATH, "//img[@src='Images/btn-envoyer.gif']", 5, 0.001)
			print "Message '", text, "' sended to '", to, "'."
			print "Sending                                                [OK]"
		else:
			print "Sending                                            [NOT OK]"
		print "---------+---------+---------+---------+---------+---------"