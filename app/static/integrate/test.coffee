test = new window.TestBuilder()
test.visit "/"
test.type "#id_email", "test_email@example.org"
test.type "#id_password1", "1231231234"
test.type "#id_password2", "1231231234"
test.click "body .signup button" 
test.assert "body"
test.run() 