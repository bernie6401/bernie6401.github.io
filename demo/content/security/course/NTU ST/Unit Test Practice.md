---
title: Unit Test Practice
tags: [NTU_ST, Software Testing, NTU]

---

# Unit Test Practice
###### tags: `NTU_ST` `Software Testing`

:::spoiler Click to open TOC
[TOC]
:::

## Install the environment
* Install Visual Studio with .NET that we can use C# language to implement unit test properly.![install c#](https://imgur.com/VwMKdZM.png)
## Create a project to test
* Create a new project and choose C# as your language and named the project **Bank**.![create project](https://imgur.com/bPDga9p.png)
* Rename Program.cs as BankAccount.cs and replace all content by the following code.
```c#
using System;

namespace BankAccountNS

    public class BankAccount
    {
        private readonly string m_customerName;
        private double m_balance;

        private BankAccount() { }

        public BankAccount(string customerName, double balance)
        {
            m_customerName = customerName;
            m_balance = balance;
        }

        public string CustomerName
        {
            get { return m_customerName; }
        }

        public double Balance
        {
            get { return m_balance; }
        }

        public void Debit(double amount)
        {
            if (amount > m_balance)
            {
                throw new ArgumentOutOfRangeException("amount");
            }

            if (amount < 0)
            {
                throw new ArgumentOutOfRangeException("amount");
            }

            m_balance += amount; // intentionally incorrect code
        }

        public void Credit(double amount)
        {
            if (amount < 0)
            {
                throw new ArgumentOutOfRangeException("amount");
            }

            m_balance += amount;
        }

        public static void Main()
        {
            BankAccount ba = new BankAccount("Mr. Bryan Walton", 11.99);

            ba.Credit(5.77);
            ba.Debit(11.22);
            Console.WriteLine("Current balance is ${0}", ba.Balance);
        }
    }
}
```
* Build it by clicking **Build Solution** in Build menu.

## Create a unit test project
* Create a new project at solution explorer and named it **BankTests**. The other part just maintain default setup.![](https://imgur.com/ryriCen.png)
* Select **MSTest Test Project**![](https://imgur.com/dI5h4T0.png)<-This is important.
* **Add reference** by selecting **Add Reference** at **BankTests/Dependencies**![](https://imgur.com/9Miqs7p.png)
* In the **Reference Manager** dialog box, expand **Projects**, select **Solution**, and then check the Bank item.![](https://imgur.com/ZBOR73N.png)

## Create the test class
* Rename UnitTest1.cs to BankAccountTests.cs and replace the original code with the following section and add using statement at the top of the class file.
```c#
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace BankTests
{
    [TestClass]
    public class BankAccountTests
    {
        [TestMethod]
        public void TestMethod1()
        {
        }
    }
}
```
* BTW, the default class part can be ignored.

## Create the first test method
* Replace the default class with the following code
```c#
[TestMethod]
public void Debit_WithValidAmount_UpdatesBalance()
{
    // Arrange
    double beginningBalance = 11.99;
    double debitAmount = 4.55;
    double expected = 7.44;
    BankAccount account = new BankAccount("Mr. Bryan Walton", beginningBalance);

    // Act
    account.Debit(debitAmount);

    // Assert
    double actual = account.Balance;
    Assert.AreEqual(expected, actual, 0.001, "Account not debited correctly");
}
```
* Analyze this part: Assert.AreEqual method will catch the exception when **expected value** unequal **actual value** or their difference larger than **delta**(0.001).
* Comparing with BankAccount.cs, the truly process of **Debit** function is $beginningBalance - debitAmount = expected$ -> $11.99 - 4.55 = 7.44$

## Build and run the test
* On the Build menu, choose Build Solution (or press Ctrl + SHIFT + B) and press **Ctrl + E, T** to open **Test Explorer**, then **Run All**.![](https://imgur.com/ljNqXiS.png)
* You'll find that all Test are failed, so you must modify somewhere incorrect.

## Fix your code and rerun your tests
* Return to BankAccount.cs and observe Debit() function.
![](https://imgur.com/sGGMxu7.png)
* Must change `m_balance += amount;` to `m_balance -= amount;`
* Build and Run the code again and you'll find the test is correct this time![](https://imgur.com/BNKS05j.png)

## Create and run new test methods
* Add the following program in test class and rebuild it.
```c#
[TestMethod]
public void Debit_WhenAmountIsLessThanZero_ShouldThrowArgumentOutOfRange()
{
    // Arrange
    double beginningBalance = 11.99;
    double debitAmount = -100.00;
    BankAccount account = new BankAccount("Mr. Bryan Walton", beginningBalance);

    // Act and assert
    Assert.ThrowsException<System.ArgumentOutOfRangeException>(() => account.Debit(debitAmount));
}

[TestMethod]
public void Debit_WhenAmountIsMoreThanBalance_ShouldThrowArgumentOutOfRange()
{
    // Arrange
    double beginningBalance = 11.99;
    double debitAmount = 200.00;
    BankAccount account = new BankAccount("Mr. Bryan Walton", beginningBalance);

    // Act and assert
    Assert.ThrowsException<System.ArgumentOutOfRangeException>(() => account.Debit(debitAmount));
}
```
* Analyze: you'll find out that the **debitAmout** in the **1st test method** is less than zero and the **debitAmount** in **2nd test method** is larger than **beginningBalance**.
* After runing test explorer, these 2 code block are working properly, but you don't know what kind of exception is(amount > m_balance or amount < 0), we just know somewhere throw back an exception message.

## Revise BankAccount.cs
* Trace back to BankAccount.Debit and you'll notice that they used the same exception, so you can determine to use ArgumentOutOfRangeException(String, Object, String) to contain the name of the argument, the argument value, and a user-defined message.
```c#
if (amount > m_balance)
{
    throw new ArgumentOutOfRangeException("amount");
}

if (amount < 0)
{
    throw new ArgumentOutOfRangeException("amount");
}
```

## Refactor the code under test
* Define 2 constants for the error message at class scope, put the following code block in the class under test, BankAccout.
```c#
public const string DebitAmountExceedsBalanceMessage = "Debit amount exceeds balance";
public const string DebitAmountLessThanZeroMessage = "Debit amount is less than zero";
```
* Then modify the 2 conditional statements in the Debit method.
```c#
if (amount > m_balance)
{
    throw new System.ArgumentOutOfRangeException("amount", amount, DebitAmountExceedsBalanceMessage);
}

if (amount < 0)
{
    throw new System.ArgumentOutOfRangeException("amount", amount, DebitAmountLessThanZeroMessage);
}
```
* Refactor test method like this. Replacing Assert.ThrowsException with using try/catch method to catch unexpected exception situation.
```C#
[TestMethod]
public void Debit_WhenAmountIsMoreThanBalance_ShouldThrowArgumentOutOfRange()
{
    // Arrange
    double beginningBalance = 11.99;
    double debitAmount = 20.0;
    BankAccount account = new BankAccount("Mr. Bryan Walton", beginningBalance);

    // Act
    try
    {
        account.Debit(debitAmount);
    }
    catch (System.ArgumentOutOfRangeException e)
    {
        // Assert
        StringAssert.Contains(e.Message, BankAccount.DebitAmountExceedsBalanceMessage);
    }
}
```

## The last part
* Not really understatnd about adding Assert.Fail at the end of the test method.

## Final Result
![](https://imgur.com/5NtqEKr.png)


## Reference
* [Microsoft Learn](https://learn.microsoft.com/zh-tw/visualstudio/test/walkthrough-creating-and-running-unit-tests-for-managed-code?view=vs-2022&source=docs)
* [IThelp-動手寫Unit Test](https://ithelp.ithome.com.tw/articles/10102643)
* [ProgressBar](https://progressbar.tw/posts/11)