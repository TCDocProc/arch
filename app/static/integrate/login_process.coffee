test = new window.TestBuilder()
test.visit "/"
test.assert "#signup_form"
test.click "body .signup button" 
test.click ".content > .branch > .sequence:nth-child(1)"
test.assert "body"
test.click "ul.right li:last a"
test.click "body button:first"
test.run() 