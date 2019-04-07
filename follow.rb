 require 'watir'
require 'awesome_print'
require_relative './_credentials'

username = $username
password = $password

to_follow = "justinbieber"

browser = Watir::Browser.new :chrome

browser.goto("https://www.instagram.com/accounts/login/")

sleep(3)
ap("logging in...please be patience\n\n --> ")

browser.text_field(:name => "username").set "#{username}"
browser.text_field(:name => "password").set "#{password}"
browser.button(:class => "_0mzm- sqdOP  L3NKy       ").click
browser.goto("https://www.instagram.com/#{to_follow}/")

if browser.button(:class => "_0mzm- sqdOP  L3NKy       ").exists?
    browser.button(:class => "_0mzm- sqdOP  L3NKy       ").click
    puts("\n Following #{to_follow}...\n\n")
    sleep(5)
else
    browser.button(:class => "aOOlW -Cab_   ").click
    puts("\n Unfollowing...")
end

sleep(200)
