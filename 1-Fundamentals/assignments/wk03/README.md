<!-- HEADER -->
<div align="center">
  <h1>Week 03: Workshop Assignment - Text-Based Donations Website</h1>
  <p>
    <img style="border: 2px solid white" src="donation.gif" alt="animated GIF of Mr. Burns from 'The Simpsons' contemplating a donation">
  </p>
  <br>
</div>
<!-- /HEADER -->
<!-- MAIN -->
<div align="center">
  <h2>The Instructions</h2>
  <p> 
    <a href="https://www.youtube.com/embed/TTh_PDOdRJo" target="_blank">
      <img src="https://i.ytimg.com/vi/TTh_PDOdRJo/hqdefault.jpg">
    </a>
  </p>
</div>
<br>
<h2 align="center">The Solution(s)</h2>
<ul>
  <li>
    <div>
      <h3><a href="./solution1/app.py">Solution #1</a></h3>
      <p>I followed the directives precisely as they were provided. All base and bonus tasks are satisfied.</p>
    </div>
  </li>
  <li>
    <div>
      <h3><a href="./solution2/app.py">Solution #2</a></h3>
      <p>The code was refactored to utilize the benefits of custom classes and inheritance. Three classes were defined in <code>user.py</code> to represent the main objects that exist within this application:<p>
      <ul>
        <li>
          <p><code>User</code>: a superclass that represents a standard user of the application</p>
        </li>
        <li>
          <p><code>Admin</code>: a subclass of <code>User</code> with additional administrative privileges</p>
        </li>
        <li>
          <p><code>Donation</code>: a representation of a donation made by any type of user</p>
        </li>
      </ul>
      <p>Some of the original application functions were converted into either instance methods (e.g. <code>donate</code>) or class methods (e.g. <code>show_donations</code>). Additional improvements were made to both aesthetics and functionality, and several features were included.</p>
      <ol>
        <li>
          <p>Only standard main menu options&mdash;<em>Login</em>, <em>Register</em>, <em>Show All Donations</em>, and <em>Exit</em>&mdash;are displayed if a user is not logged in.
          <ul>
            <li>a logged in <code>User</code> has all standard options and also <em>Make Donation</em>, <em>View My Donations</em>, and <em>Logout</em></li>
            <li>a logged in <code>Admin</code> has all <code>User</code> options and also <em>Administrative Settings</em></li>
          </ul></p>
        </li>
        <li>
          <div>
            <p><em>Show All Donations</em> : If a user is logged in, the username is replaced with the prounoun "you" for any self-made donations. Also, a timestamp for when a donation was made is displayed for all records.</p>
          </div>
        </li>
        <li>
          <div>
            <p><em>View My Donations</em> : A list of donations made solely by the logged in user is displayed.</p>
          </div>
        </li>
        <li>
          <div>
            <p><em>Logout</em> : Logs a user out of the current session, and displays the main menu with standard options only.</p>
          </div>
        </li>
        <li>
          <div>
            <p><em>Administrative Settings</em></p>
            <ul>
              <li>
                <p><em>Change User Password</em> : Allows an <code>Admin</code> to change the password for any registered user.</p>
              </li>
              <li>
                <p><em>Change User Privileges</em> : Allows an <code>Admin</code> to promote a standard user to an administrator, or demote an administrator to a standard user. The program will prevent an administrator from being demoted if there is only one registered administrator in the database.</p>
              </li>
            </ul>
          </div>
        </li>
      </ol>
    </div>
  </li>
</ul>
<br>
<hr>
<!-- /MAIN -->
<!-- FOOTER -->
<div align="center">
  <p>Feel free to contact me if you have any questions, comments, or concerns.</p>
  <span>
    <a href="mailto:jdwill917@live.com">
      <img src="https://img.shields.io/badge/Email-%230078D4.svg?&style=for-the-badge&logo=microsoftoutlook&logoColor=white&labelColor=000000&color=6495ED&link=mailto:jdwill917@live.com">
    </a>
  </span>
  <span>
    <a href="https://www.instagram.com/jdthedev" target="_blank">
      <img src="https://img.shields.io/badge/Instagram-%23E4405F.svg?&style=for-the-badge&logo=instagram&logoColor=white&labelColor=000000&color=6495ED&link=https://www.instagram.com/jdthedev">
    </a>
  </span> 
  <span>
    <a href="https://twitter.com/jd_the_dev" target="_blank">
      <img src="https://img.shields.io/badge/Twitter-%231877F2.svg?&style=for-the-badge&logo=twitter&logoColor=white&labelColor=000000&color=6495ED&link=https://twitter.com/jd_the_dev">
    </a>
  </span>
  <br>
  <br>
  <blockquote>
    Be not simply good; be good for something. -Henry David Thoreau, <em>Letters to H.G.O. Blake</em>
  </blockquote>
</div>
<!-- /FOOTER -->
