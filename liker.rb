  require 'watir'
require_relative './_credentials'

# define name and password
username = $username
password = $password

# defining dedaults
like_counter = 0
num_rounds = 0
MAX_LIKES = 150
# opening browser0
browser = Watir::Browser.new :chrome
browser.goto("https://www.instagram.com/accounts/login")
printf("\n\n Logging please wait...Be patience...\n\n")

# setting username an password
browser.text_field(:name => "username").set "#{username}"
browser.text_field(:name => "password").set "#{password}"

# clicking the "login" button
browser.button(:class => "_0mzm- sqdOP  L3NKy       ").click
printf("\n\n Whoaaa! We're in dat CrawlLife...\n")
# now to like part comes
printf("\n\n Making Soup ingredients...\n")
sleep(2)

loop do
# scrolling events
3.times do |i| browser.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
sleep(3)
end

# condition
  if browser.span(:class => "glyphsSpriteHeart__outline__24__grey_9 u-__7").exists?
    browser.spans(:class => "glyphsSpriteHeart__outline__24__grey_9 u-__7").each {|l|
      l.click
      like_counter += 1
      }
    printf("\n.. Photos Liked :: #{like_counter}")
  else
    printf ("\n...No media to like rn, yo. Sorry homie, we tried...\n")
end
    num_rounds += 1
    printf("\n... No Of Rounds ==>  #{num_rounds}\n")
  break if like_counter >= MAX_LIKES
    sleep(20)
end


# hold the program
sleep(10)
