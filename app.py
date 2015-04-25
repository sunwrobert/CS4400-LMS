import pymysql
from flask import Flask, request, render_template, redirect, url_for, flash, session
from datetime import timedelta
import datetime
 
app = Flask(__name__)
connection = pymysql.connect(host='localhost',
                             user='root',
                             passwd='admin',
                             db='CS4400',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
 
@app.route('/')
def main():
    if 'username' in session:
        return redirect(url_for('home',user=determineUserType(session['username'])))
    return redirect('login')
 
def determineUserType(username):
    sql = "SELECT Username FROM staff WHERE Username = '{username}'".format(username=username)
    result = cursor.execute(sql)
    if result:
        return 'staff'
    sql = "SELECT Username FROM student_faculty WHERE Username = '{username}' AND IsFaculty = 1".format(username=username)
    result = cursor.execute(sql)
    if result:
        return 'faculty'
    return 'students'
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        sql = ("SELECT Username FROM user WHERE Username = '{user}' \
                AND Password = '{password}';"
               .format(user=request.form['username'], password=request.form['password']))
        result = cursor.execute(sql)
        if result:
            row = cursor.fetchone()
            session['username'] = row.get('Username')
            return redirect(url_for('home',user=determineUserType(session['username'])))
        else:
            flash("Incorrect login!", 'alert-error')
 
    return render_template('login.html')
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['password'] != request.form ['confirmPassword']:
            flash("Passwords don't match!", 'alert-error')
        else:
            sql = ("INSERT INTO user VALUES('{u}','{p}')"
                   .format(u=request.form['username'], p=request.form['password']))
            try:
                cursor.execute(sql)
                connection.commit()
                session['username'] = request.form['username']
                return redirect('createProfile')
            except pymysql.err.IntegrityError:
                flash("Username already exists!", 'alert-error')
    return render_template('register.html')
 
@app.route('/createProfile', methods=['GET', 'POST'])
def createProfile():
    if request.method == 'POST':
        dept = request.form['dept']
        if (request.form['dept'] == ''):
            dept = "NULL"
        print(request.form['isFaculty'])
        sql = ("INSERT INTO student_faculty VALUES('{userName}','{fullName}', STR_TO_DATE('{dob}', '%m/%d/%Y'), \
        '{gender}',0, '{email}', '{address}','{isFaculty}', 0, '{dept}');".format(userName=session['username'],
                    fullName=request.form['firstName'] + " " + request.form['lastName'],
                    dob=request.form['dob'],
                    gender=request.form['gender'][:1],
                    email=request.form['email'],
                    address=request.form['address'],
                    isFaculty=int(request.form['isFaculty']),
                    dept=dept))
 
        try:
            cursor.execute(sql)
            connection.commit()
            return redirect(url_for('home',user=determineUserType(session['username'])))
        except:
            flash("An unknown error occurred!")
 
    return render_template('createProfile.html')
 
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html',user=determineUserType(session['username']))
 
@app.route('/searchBooks', methods=['GET', 'POST'])
def searchBooks():
    session['rows'] = ''
    session['reserve'] = ''
    if request.method == 'POST':
        sql = "SELECT DISTINCT book.ISBN, book.Title, \
                 book.Edition FROM book INNER JOIN book_authors ON \
                 book.ISBN = book_authors.ISBN "
        reserveSql = sql
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        if isbn and title and author:
            sql += "WHERE book.ISBN LIKE '%{isbn}%' AND book.Title LIKE '%{title}%' \
                 AND book_authors.Author LIKE '%{author}%'".format(isbn=isbn,title=title,author=author)
            reserveSql += "WHERE book.ISBN LIKE '%{isbn}%' AND book.Title LIKE '%{title}%' \
                 AND book_authors.Author LIKE '%{author}%'".format(isbn=isbn,title=title,author=author)
        elif isbn and title:
            sql += "WHERE book.ISBN LIKE '%{isbn}%' AND book.Title LIKE '%{title}%'".format(isbn=isbn,title=title)
            reserveSql += "WHERE book.ISBN LIKE '%{isbn}%' AND book.Title LIKE '%{title}%'".format(isbn=isbn,title=title)
        elif isbn and author:
            sql += "WHERE book.ISBN LIKE '%{isbn}%' AND book.Author LIKE '%{author}%'".format(isbn=isbn,author=author)
            reserveSql += "WHERE book.ISBN LIKE '%{isbn}%' AND book_authors.Author LIKE '%{author}%'".format(isbn=isbn,author=author)
        elif title and author:
            sql += "WHERE book.Title LIKE '%{title}%' AND book_authors.Author LIKE '%{author}%'".format(title=title,author=author)
            reserveSql += "WHERE book.title LIKE '%{title}%' AND book_authors.Author LIKE '%{author}%'".format(title=title,author=author)
        elif isbn:
            sql += "WHERE book.ISBN LIKE '%{isbn}%'".format(isbn=isbn)
            reserveSql += "WHERE book.ISBN LIKE '%{isbn}%'".format(isbn=isbn)
        elif title:
            sql += "WHERE book.Title LIKE '%{title}%'".format(title=title)
            reserveSql += "WHERE book.Title LIKE '%{title}%'".format(title=title)
        elif author:
            sql += "WHERE book_authors.Author LIKE '%{author}%'".format(author=author)
            reserveSql += "WHERE book_authors.Author LIKE '%{author}%'".format(author=author)
 
        sql += " AND book.IsBookOnReserve = '0';"
        reserveSql += " AND book.IsBookOnReserve = '1';"
        cursor.execute(sql)
        rows = cursor.fetchall()
        session['sql'] = sql
        cursor.execute(reserveSql)
        reserveRows = cursor.fetchall()
        if rows:
            for x in range(len(rows)):
                sql = "SELECT COUNT(CopyNumber) from book_copy WHERE ISBN = '{isbn}' \
                AND IsOnHold = 0 AND IsCheckedOut = 0 AND IsDamaged = 0;".format(isbn=rows[x].get('ISBN'))
                cursor.execute(sql)
                countRows = cursor.fetchone()
                count = countRows.get('COUNT(CopyNumber)')
                rows[x]['Copies'] = count
            session['rows'] = rows
        if reserveRows:
            for x in range(len(reserveRows)):
                sql = "SELECT COUNT(CopyNumber) from book_copy WHERE ISBN = '{isbn}' \
                AND IsOnHold = 0 AND IsCheckedOut = 0 AND IsDamaged = 0;".format(isbn=reserveRows[x].get('ISBN'))
                cursor.execute(sql)
                countRows = cursor.fetchone()
                count = countRows.get('COUNT(CopyNumber)')
                reserveRows[x]['Copies'] = count
            session['reserve'] = reserveRows
        if not rows and not reserveRows:
            flash("There are no books that match your request")
        else:
            return redirect(url_for('holdRequest',rows=rows,reserve=reserveRows))
    return render_template('searchBooks.html')
 
def calculateRows(sql):
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows:
        for x in range(len(rows)):
            sql = "SELECT COUNT(CopyNumber) from book_copy WHERE ISBN = '{isbn}' \
            AND IsOnHold = 0 AND IsCheckedOut = 0 AND IsDamaged = 0;".format(isbn=rows[x].get('ISBN'))
            cursor.execute(sql)
            countRows = cursor.fetchone()
            count = countRows.get('COUNT(CopyNumber)')
            rows[x]['Copies'] = count
    return rows
 
 
@app.route('/damagedReport', methods=['GET', 'POST'])
def damagedReport():
    if request.method == 'POST':
        month = request.form['month']
        subject1 = request.form['subject1']
        subject2 = request.form['subject2']
        subject3 = request.form['subject3']
        sql = "SELECT MONTHNAME(issue.ReturnDate) AS Month, book.SubjectName as Subject, COUNT(book_copy.isDamaged)" \
              " AS DamagedBooks  FROM book INNER JOIN book_copy ON book.ISBN = book_copy.ISBN INNER JOIN issue ON" \
              " issue.ISBN = book_copy.ISBN AND issue.CopyNumber = book_copy.CopyNumber WHERE MONTHNAME(issue.ReturnDate) = '{month}' AND " \
              "(book.SubjectName = '{subject1}' OR book.SubjectName = '{subject2}' OR book.SubjectName = '{subject3}')" \
              " AND book_copy.IsDamaged = 1 GROUP BY Subject;".format(month=month, subject1=subject1, subject2=subject2, subject3=subject3)
        if not month:
            flash("Please select a month")
        elif not subject1 and not subject2 and not subject3:
            flash("Please select a month and at least one subject")
        else:
            cursor.execute(sql)
            rows = cursor.fetchall()
            print(rows)
            if rows:
                return render_template('damagedReport.html', rows=rows, month=month)
            else:
                flash("There were no damaged books returned in {month} for those subjects".format(month=month))
    return render_template('damagedReport.html')
 
 
@app.route('/popularBooksReport', methods=['GET', 'POST'])
def popularBooksReport():
    sql = "(SELECT MONTHNAME(issue.IssueDate) AS Month, book.Title AS Title, COUNT(issue.IssueDate) as Checkouts " \
          "FROM book INNER JOIN book_copy ON book.ISBN = book_Copy.ISBN INNER JOIN issue ON issue.ISBN = book_copy.ISBN" \
          " AND issue.CopyNumber = book_copy.CopyNumber WHERE (MONTHNAME(issue.IssueDate) = 'January') " \
          "GROUP BY book.Title ORDER BY Checkouts DESC LIMIT 3) UNION ALL " \
          "(SELECT MONTHNAME(issue.IssueDate) AS Month, book.Title AS Title, COUNT(issue.IssueDate) as Checkouts " \
          "FROM book INNER JOIN book_copy ON book.ISBN = book_Copy.ISBN INNER JOIN issue ON issue.ISBN = book_copy.ISBN" \
          " AND issue.CopyNumber = book_copy.CopyNumber WHERE (MONTHNAME(issue.IssueDate) = 'February') " \
          "GROUP BY book.Title ORDER BY Checkouts DESC LIMIT 3);"
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows:
        if(len(rows)) == 1:
            return render_template('popularBooksReport.html', rows=rows)
        else:
            currMonth = rows[0].get('Month')
            for x in range(1, len(rows)):
                temp = currMonth
                currMonth = rows[x].get('Month')
                if temp == currMonth:
                    rows[x]['Month'] = ''
            return render_template('popularBooksReport.html', rows=rows)
    else:
        flash("There were no books checked out in January or February")
    return render_template('popularBooksReport.html')
 
@app.route('/frequentReport', methods=['GET', 'POST'])
def frequentReport():
    sql = "(SELECT MONTHNAME(issue.IssueDate) AS Month, student_faculty.Name, COUNT(issue.IssueDate) as Checkouts FROM " \
          "issue INNER JOIN student_faculty ON issue.Username = student_faculty.Username WHERE MONTHNAME(issue.IssueDate)" \
          " = 'January' GROUP BY student_faculty.username HAVING Checkouts > 10 ORDER BY Checkouts DESC LIMIT 5) UNION ALL" \
          " (SELECT MONTHNAME(issue.IssueDate) AS Month, student_faculty.Name, COUNT(issue.IssueDate) as Checkouts FROM issue" \
          " INNER JOIN student_faculty ON issue.Username = student_faculty.Username WHERE MONTHNAME(issue.IssueDate) = 'February'" \
          " GROUP BY student_faculty.username HAVING Checkouts > 10 ORDER BY Checkouts DESC LIMIT 5)"
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows:
        if(len(rows)) == 1:
            return render_template('frequentReport.html', rows=rows)
        else:
            currMonth = rows[0  ].get('Month')
            for x in range(1, len(rows)):
                temp = currMonth
                currMonth = rows[x].get('Month')
                if temp == currMonth:
                    rows[x]['Month'] = ''
            return render_template('frequentReport.html', rows=rows)
    else:
        flash("No users checked out more than 10 books in January and February")
    return render_template('frequentReport.html')
 
 
@app.route('/popularSubjectReport', methods=['GET', 'POST'])
def popularSubjectReport():
    sql = "(SELECT MONTHNAME(issue.IssueDate) AS Month, book.SubjectName, COUNT(issue.IssueDate) as Checkouts FROM issue" \
          " INNER JOIN book ON issue.ISBN = book.isbn WHERE MONTHNAME(issue.IssueDate) = 'January' GROUP BY book.SubjectName ORDER BY Checkouts DESC LIMIT 3)" \
          " UNION ALL " \
          "(SELECT MONTHNAME(issue.IssueDate) AS Month, book.SubjectName, COUNT(issue.IssueDate) as Checkouts FROM issue" \
          " INNER JOIN book ON issue.ISBN = book.isbn WHERE MONTHNAME(issue.IssueDate) = 'February' GROUP BY book.SubjectName ORDER BY Checkouts DESC LIMIT 3)"
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows:
        if(len(rows)) == 1:
            return render_template('popularSubjectReport.html', rows=rows)
        else:
            currMonth = rows[0].get('Month')
            for x in range(1, len(rows)):
                temp = currMonth
                currMonth = rows[x].get('Month')
                if temp == currMonth:
                    rows[x]['Month'] = ''
            return render_template('popularSubjectReport.html', rows=rows)
    else:
        flash("No books were checked out in January and February")
    return render_template('popularSubjectReport.html')
 
@app.route('/holdRequest', methods=['GET', 'POST'])
def holdRequest():
    sql = session['sql']
    rows = session['rows']
    reserve = session['reserve']
    if request.method == 'POST':
        isbn = request.form['selectedBook']
        sql = "UPDATE book_copy SET IsOnHold = 1 WHERE ISBN = '{isbn}' AND \
                CopyNumber=(SELECT * FROM(SELECT CopyNumber FROM book_copy WHERE ISBN='{isbn}' \
                AND IsOnHold=0 AND IsCheckedOut = 0 AND IsDamaged = 0 GROUP BY CopyNumber LIMIT 1)temp);".format(isbn=isbn)
        limitOneBookSql = "SELECT * FROM issue INNER JOIN book_copy on book_copy.ISBN = issue.ISBN and book_copy.CopyNumber = issue.CopyNumber \
WHERE issue.ISBN = '{isbn}' AND Username = '{userName}' and IsOnHold=1;".format(isbn=isbn,userName=session['username'])
        cursor.execute(limitOneBookSql)
        row = cursor.fetchone()
        if row:
            flash('Cannot have multiple hold requests on the same book!')
        else:
            issueSql = "INSERT INTO issue VALUES('{userName}',0,'{isbn}',(SELECT CopyNumber from book_copy where IsOnHold = 1 \
                AND ISBN='{isbn}' ORDER BY CopyNumber DESC LIMIT 1),CURDATE(),CURDATE(),DATE_ADD(CURDATE(), INTERVAL 17 DAY),0);" \
                .format(userName=session['username'], isbn=isbn)
            try:
                cursor.execute(sql)
                cursor.execute(issueSql)
                connection.commit()
                sql = "SELECT IssueID FROM issue ORDER BY IssueID DESC LIMIT 1;"
                cursor.execute(sql)
                row = cursor.fetchone()
                issueID = row.get('IssueID')
                flash("Hold successful! Your Issue ID is: " + str(issueID))
            except:
                flash('Something wrong happened.')
                sql = session['sql']
                rows = calculateRows(sql)
            sql = session['sql']
            rows = calculateRows(sql)
            return render_template('holdRequest.html', rows=rows, reserve=reserve,success=True)
    sql = session['sql']       
    rows = calculateRows(sql)
    return render_template('holdRequest.html', rows=rows, reserve=reserve)
 
@app.route('/bookCheckout',methods=['GET','POST'])
def bookCheckout():
    if request.method == 'POST':
        if request.form.get('buttonOne', None) == "Submit":
            issueID = request.form['issueID']
            expiredHoldSql = "SELECT * FROM issue WHERE DATEDIFF(CURDATE(),IssueDate) > 3 \
            AND IssueID= {issueID}".format(issueID=issueID)
            results = cursor.execute(expiredHoldSql)
            if results:
                flash("This hold has expired!")
            else:
                if issueID:
                    sql = "SELECT Username, issue.ISBN, issue.CopyNumber FROM issue inner join book_copy ON \
                    book_copy.ISBN = issue.ISBN and book_copy.CopyNumber = issue.CopyNumber \
                    where IssueID = {issueID} and IsOnHold=1".format(issueID=request.form['issueID'])
                    results = cursor.execute(sql)
                    if results:
                        row = cursor.fetchone()
                        username = row.get('Username')
                        isbn = row.get('ISBN')
                        copyNumber = row.get('CopyNumber')
                        checkOutDate = datetime.datetime.today()
                        estimatedReturnDate = checkOutDate + timedelta(days=14)
                        return render_template('bookCheckout.html', issueID=issueID,
                            username=username,isbn=isbn,copyNumber=copyNumber,checkOutDate=checkOutDate.strftime("%m/%d/%y"),
                            estimatedReturnDate=estimatedReturnDate.strftime("%m/%d/%y"))
                    else:
                        flash("No current hold was found for this issue!")
                else:
                    flash("Please enter a valid issue ID")
 
        elif request.form.get('buttonTwo', None) == "Confirm":
            issueID = request.form['issueID']
            isbn = request.form['isbn']
            copyNumber = request.form['copyNumber']
            returnDate = datetime.datetime.today() + timedelta(days=14)
            try:
                sql = "UPDATE issue SET ReturnDate='{returnDate}' WHERE IssueID={issueID}".format(issueID=issueID,returnDate=returnDate)
                cursor.execute(sql)
                sql = "UPDATE book_copy SET IsOnHold=0,IsCheckedOut=1 WHERE ISBN='{isbn}' AND CopyNumber={copyNumber} \
                    ".format(isbn=isbn,copyNumber=copyNumber)
                cursor.execute(sql)
                connection.commit()
                flash("Book successfully checked out!")
            except:
                flash("An unknown error occurred")
 
    return render_template('bookCheckout.html')
 
@app.route('/lostDamagedBook',methods=['GET','POST'])
def lostDamagedBook():
    if request.method == 'POST':
        if request.form.get('buttonOne', None) == "Look for the last user":
            isbn = request.form['isbn']
            copyNumber = request.form['copyNumber']
            currentTime = datetime.datetime.today()
            if isbn and copyNumber:
                sql = "SELECT IssueDate, Username FROM issue WHERE ISBN='{isbn}' AND CopyNumber={copyNumber} \
                ORDER BY IssueDate DESC LIMIT 1".format(isbn=isbn,copyNumber=copyNumber)
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    lastUser = result.get('Username')
                    sql = "SELECT Cost FROM book WHERE ISBN='{isbn}'".format(isbn=isbn)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    amountCharged = result.get('Cost') / 2
                    return render_template('lostDamagedBook.html',lastUser=lastUser,amountCharged=amountCharged)
                else:
                    flash("No user found corresponding to this book!")
            else:
                flash("Please enter a valid ISBN and Book Copy #")
        elif request.form.get('buttonTwo', None) == "Confirm":
            penalty = int(request.form['amountCharged'])
            lastUser = request.form['lastUser']
            isbn = request.form['isbn']
            copyNumber = request.form['copyNumber']
            try:
                sql = "UPDATE student_faculty SET Penalty = Penalty + {penalty} WHERE Username = '{lastUser}' \
                ".format(penalty=penalty,lastUser=lastUser)
                cursor.execute(sql)
                sql = "UPDATE book_copy SET IsOnHold=0, IsCheckedOut=0, IsDamaged=1 WHERE ISBN='{isbn}' \
                AND CopyNumber={copyNumber}".format(isbn=isbn,copyNumber=copyNumber)
                connection.commit()
                flash("Charge successfully added to user.")
            except:
                flash("An unknown error occurred.")
    return render_template('lostDamagedBook.html')
 
@app.route('/returnBook',methods=['GET','POST'])
def returnBook():
    if request.method == 'POST':
        if request.form.get('buttonOne', None) == "Submit":
            issueID = request.form['issueID']
            if issueID:
                sql = "SELECT Username, issue.CopyNumber, issue.ISBN \
                FROM issue INNER JOIN book_copy on book_copy.ISBN = issue.ISBN and book_copy.CopyNumber = issue.CopyNumber \
                WHERE IssueID={issueID} and isCheckedOut=1".format(issueID=issueID)
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    username = result.get('Username')
                    copyNumber = result.get('CopyNumber')
                    isbn = result.get('ISBN')
                    return render_template('returnBook.html',issueID=issueID,isbn=isbn,copyNumber=copyNumber,username=username)
                else:
                    flash("Please enter an issue that pertains to a book that is checked out!")
            else:
                flash("Please enter a valid issue ID")
 
        elif request.form.get('buttonTwo', None) == "Confirm":
            isbn = request.form['isbn']
            copyNumber = request.form['copyNumber']
            damagedResult = request.form['isDamaged']
 
            username = request.form['username']
            damaged = 0
            if (damagedResult == 'Y'):
                damaged = 1
            username = request.form['username']
            try:
                sql = "UPDATE book_copy SET IsCheckedOut=0,IsDamaged='{damaged}' WHERE ISBN='{isbn}' AND \
                CopyNumber={copyNumber}".format(damaged=damaged,isbn=isbn,copyNumber=copyNumber)
                cursor.execute(sql)
                sql = "SELECT DATEDIFF(CURDATE(),ReturnDate) "
                sql = "UPDATE student_faculty INNER JOIN issue ON issue.Username = student_faculty.Username \
                SET Penalty = Penalty + 0.5 * DATEDIFF(CURDATE(),ReturnDate) WHERE student_faculty.Username \
                ='{username}' AND DATEDIFF(CURDATE(),ReturnDate) > 0".format(username=username)
                cursor.execute(sql)
                connection.commit()
                flash("Book successfully returned")
            except:
                flash("An unknown error occurred")
 
    return render_template('returnBook.html')
 
@app.route('/requestExtension', methods=['GET', 'POST'])
def requestExtension():
    if request.method == 'POST':
        if request.form.get('buttonOne', None) == "Submit":
            issueID = request.form['issueID']
            # session['issueID'] = issueID
            if issueID:
                sql = "SELECT issue.Username, issue.IssueDate, issue.ExtensionDate, issue.ReturnDate, issue.ExtensionCount, " \
                      "book_copy.FutureRequester, student_faculty.IsFaculty FROM issue INNER JOIN book_copy ON " \
                      "(issue.ISBN = book_copy.ISBN AND issue.CopyNumber = book_copy.CopyNumber) " \
                      "INNER JOIN student_faculty ON issue.Username = student_faculty.Username WHERE issue.IssueID = '{issueID}' " \
                      "AND issue.Username = '{username}' AND book_copy.IsCheckedOut=1;". \
                    format(issueID=issueID, username=session['username'])
                results = cursor.execute(sql)
                if results:
                    row = cursor.fetchone()
                    maxExtension = 0
                    extensionCount = row.get('ExtensionCount')
                    futureRequester = row.get('FutureRequester')
                    issueDate = row.get('IssueDate')
                    returnDate = row.get('ReturnDate')
                    extensionDate = row.get('ExtensionDate')
                    newExtensionDate = datetime.datetime.today()
                    isFaculty = row.get('IsFaculty')
                    if isFaculty == '1':
                        maxExtension = 5
                        latestReturnDate = issueDate + timedelta(days=56)
                    elif isFaculty == '0':
                        maxExtension = 2
                        latestReturnDate = issueDate + timedelta(days=28)
                    print(maxExtension)
                    print(isFaculty)
                    newEstimatedReturnDate = newExtensionDate + timedelta(days=14)
                    if newEstimatedReturnDate >= latestReturnDate:
                        newEstimatedReturnDate = latestReturnDate
                    return render_template('requestExtension.html', issueID=issueID,
                                           originalCheckoutDate=issueDate.strftime("%m/%d/%y"),
                                           currentExtensionDate=extensionDate.strftime("%m/%d/%y"),
                                           currentReturnDate=returnDate.strftime("%m/%d/%y"),
                                           newExtensionDate=newExtensionDate.strftime("%m/%d/%y"),
                                           newEstimatedReturnDate=newEstimatedReturnDate.strftime("%m/%d/%y"))
                else:
                    flash("Issue not associated with your account or it is not checked out!")
            else:
                flash("Please enter a valid issue ID")
        elif request.form.get('buttonTwo', None) == "Request Extension":
            issueID = request.form['issueID']
            if issueID:
                sql = "SELECT issue.Username, issue.IssueDate, issue.ExtensionDate, issue.ReturnDate, issue.ExtensionCount, " \
                      "book_copy.FutureRequester, student_faculty.IsFaculty FROM issue INNER JOIN book_copy ON " \
                      "(issue.ISBN = book_copy.ISBN AND issue.CopyNumber = book_copy.CopyNumber) " \
                      "INNER JOIN student_faculty ON issue.Username = student_faculty.Username WHERE issue.IssueID = '{issueID}' " \
                      "AND issue.Username = '{username}';". \
                    format(issueID=issueID, username=session['username'])
                results = cursor.execute(sql)
                if results:
                    row = cursor.fetchone()
                    maxExtension = 0
                    extensionCount = row.get('ExtensionCount')
                    futureRequester = row.get('FutureRequester')
                    issueDate = row.get('IssueDate')
                    returnDate = row.get('ReturnDate')
                    extensionDate = row.get('ExtensionDate')
                    newExtensionDate = datetime.datetime.today()
                    isFaculty = row.get('IsFaculty')
                    if isFaculty == '1':
                        maxExtension = 5
                        latestReturnDate = issueDate + timedelta(days=56)
                    elif isFaculty == '0':
                        maxExtension = 2
                        latestReturnDate = issueDate + timedelta(days=28)
                    print(futureRequester is not None)
                    newEstimatedReturnDate = newExtensionDate + timedelta(days=14)
                    if newEstimatedReturnDate >= latestReturnDate:
                        newEstimatedReturnDate = latestReturnDate
                    if extensionCount >= maxExtension:
                        flash("Extension denied! You have requested too many extensions: {extensionCount}".format(
                            extensionCount=extensionCount))
                    elif futureRequester is not None:
                        flash("Extension denied! Your book already has a future requester")
                    elif newExtensionDate >= latestReturnDate:
                        flash("Extension denied! You can't request an extension on a book after the latest return date")
                    else:
                        updateSQL = "UPDATE issue SET ExtensionDate = '{newExtensionDate}', ReturnDate = '{newEstimatedReturnDate}', " \
                                    "ExtensionCount = '{extensionCount}' WHERE IssueID = '{issueID}' AND Username = '{username}';" \
                            .format(newExtensionDate=newExtensionDate, newEstimatedReturnDate=newEstimatedReturnDate,
                                    extensionCount=extensionCount + 1, issueID=issueID, username=session['username'])
                        cursor.execute(updateSQL)
                        connection.commit()
                        flash("Successfully added an extension!")
                    return render_template('requestExtension.html', issueID=issueID,
                                           originalCheckoutDate=issueDate.strftime("%m/%d/%y"),
                                           currentExtensionDate=extensionDate.strftime("%m/%d/%y"),
                                           currentReturnDate=returnDate.strftime("%m/%d/%y"),
                                           newExtensionDate=newExtensionDate.strftime("%m/%d/%y"),
                                           newEstimatedReturnDate=newEstimatedReturnDate.strftime("%m/%d/%y"))
                else:
                    flash("Issue not associated with your account!")
            else:
                flash("Please enter a valid issue ID")
    return render_template('requestExtension.html')
 
 
@app.route('/futureHoldRequest', methods=['GET', 'POST'])
def futureHoldRequest():
    if request.method == 'POST':
        if request.form.get('buttonOne', None) == "Request":
            isbn = request.form['isbn']
            if isbn:
                sql = "SELECT CopyNumber FROM book_copy WHERE ISBN = '{isbn}' AND IsOnHold = 0 AND IsCheckedOut = 0" \
                      " AND IsDamaged = 0 AND FutureRequester IS NULL".format(isbn=isbn)
                try:
                    result=cursor.execute(sql)
                    if result:
                        row = cursor.fetchone()
                        copyNumber = row.get('CopyNumber')
                        returnDate = datetime.datetime.today()
                        return render_template('futureHoldRequest.html',isbn=isbn, copyNumber=copyNumber, expectedAvailableDate=returnDate.strftime("%m/%d/%y"))
                    else:
                        sql = "SELECT book_copy.CopyNumber, issue.ReturnDate  FROM issue INNER JOIN book_copy ON \
                              book_copy.ISBN = issue.ISBN WHERE issue.ISBN = '{isbn}' AND issue.ReturnDate >= Now() \
                              AND (book_copy.IsCheckedOut = 1 OR book_copy.IsOnHold = 1) AND book_copy.FutureRequester IS NULL \
                              ORDER BY issue.ReturnDate ASC LIMIT 1;".format(isbn=isbn)
                        result = cursor.execute(sql)
                        if result:
                            row = cursor.fetchone()
                            copyNumber = row.get('CopyNumber')
                            returnDate = row.get('ReturnDate')
                            return render_template('futureHoldRequest.html',isbn=isbn, copyNumber=copyNumber, expectedAvailableDate=returnDate.strftime("%m/%d/%y"))
                        else:
                            flash("There are no books available to future request")
                            return render_template('futureHoldRequest.html',isbn=isbn)
                except:
                    flash("An unknown error occurred!")
            else:
                flash("Please enter a valid ISBN")
        if request.form.get('buttonTwo', None) == "Confirm":
            isbn = request.form['isbn']
            if isbn:
                sql = "SELECT CopyNumber FROM book_copy WHERE ISBN = '{isbn}' AND IsOnHold = 0 AND IsCheckedOut = 0" \
                      " AND IsDamaged = 0 AND FutureRequester IS NULL".format(isbn=isbn)
                try:
                    result=cursor.execute(sql)
                    if result:
                        row = cursor.fetchone()
                        copyNumber = row.get('CopyNumber')
                        returnDate = datetime.datetime.today()
                        updateSQL = "UPDATE book_copy SET FutureRequester = '{username}' WHERE ISBN = '{isbn}'" \
                                    " AND CopyNumber = '{copyNumber}';".format(username=session['username'], isbn=isbn,
                                                                               copyNumber=copyNumber)
                        cursor.execute(updateSQL)
                        connection.commit()
                        flash("Successfully registered yourself as future requester!")
                        return render_template('futureHoldRequest.html', isbn=isbn, copyNumber=copyNumber,
                                               expectedAvailableDate=returnDate.strftime("%m/%d/%y"))
                    else:
                        sql = "SELECT book_copy.CopyNumber, issue.ReturnDate  FROM issue INNER JOIN book_copy ON \
                                book_copy.ISBN = issue.ISBN WHERE issue.ISBN = '{isbn}' AND issue.ReturnDate >= Now() \
                                AND (book_copy.IsCheckedOut = 1 OR book_copy.IsOnHold = 1) AND book_copy.FutureRequester IS NULL  \
                                ORDER BY issue.ReturnDate ASC LIMIT 1;".format(isbn=isbn)
                        try:
                            result = cursor.execute(sql)
                            if result:
                                row = cursor.fetchone()
                                copyNumber = row.get('CopyNumber')
                                returnDate = row.get('ReturnDate')
                                updateSQL = "UPDATE book_copy SET FutureRequester = '{username}' WHERE ISBN = '{isbn}'" \
                                            " AND CopyNumber = '{copyNumber}';".format(username=session['username'], isbn=isbn,
                                                                                       copyNumber=copyNumber)
                                cursor.execute(updateSQL)
                                connection.commit()
                                flash("Successfully registered yourself as future requester!")
                                return render_template('futureHoldRequest.html', isbn=isbn, copyNumber=copyNumber,
                                                       expectedAvailableDate=returnDate.strftime("%m/%d/%y"))
                            else:
                                flash("No books available")
                                return render_template('futureHoldRequest.html', isbn=isbn)
                        except:
                            flash("Please enter a valid ISBN")
                            return render_template('futureHoldRequest.html', isbn=isbn)
                except:
                    flash("Please enter a valid ISBN")
                    return render_template('futureHoldRequest.html',isbn=isbn)
            else:
                flash("Please enter a valid ISBN")
 
    return render_template('futureHoldRequest.html')
 
 
@app.route('/trackBookLocation', methods=['GET', 'POST'])
def trackBookLocation():
    if request.method == 'POST':
        isbn = request.form['isbn']
        if isbn:
            sql = "SELECT shelf.FloorNumber, shelf.ShelfNumber, shelf.AisleNumber, book.SubjectName FROM book " \
                  "INNER JOIN shelf ON book.ShelfNumber = shelf.ShelfNumber WHERE ISBN = '{isbn}';".format(isbn=isbn)
            try:
                result = cursor.execute(sql)
                if result:
                    row = cursor.fetchone()
                    floorNumber = row.get('FloorNumber')
                    shelfNumber = row.get('ShelfNumber')
                    aisleNumber = row.get('AisleNumber')
                    subjectName = row.get('SubjectName')
                    return render_template('trackBookLocation.html', isbn=isbn, floorNumber=floorNumber, shelfNumber=shelfNumber,
                                           aisleNumber=aisleNumber, subjectName=subjectName)
            except:
                flash("Please enter a valid book ISBN")
            else:
                flash("Book location could not be determined")
        else:
            flash("Please enter a valid book ISBN")
 
    return render_template('trackBookLocation.html')
 
 
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username')
    flash('Successfully logged out!')
    return redirect('login')
 
 
if __name__ == '__main__':
    app.secret_key = 'lzboevhgsf'
    app.run(debug=True)