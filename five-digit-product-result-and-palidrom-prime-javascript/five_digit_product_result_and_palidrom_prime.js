/*
 * The task description:
 *
 *   Find biggest number that
 *     a) is a palindrome
 *     b) is a result of a multiplication of two five-digit numbers
 *
 * Time spent: ~3h
 */

/*
 *  Poor man's unit tests
 *  =====================
 */

function assertTrue(boolean) {
  if (boolean) {
    console.log('.');
  } else {
    console.log('F');
  }
}

assertTrue(isPalindrome('') === true);
assertTrue(isPalindrome(123456789 + '') === false);
assertTrue(isPalindrome(1234321+'') === true);
assertTrue(isPalindrome('123321') === true);


/*
 *   Functions
 *   =========
 */
function findMaxPalidromeProductOf5DigitMultiplication() {

  function findMaxProductPalindrome(lowerBound, upperBound) {

    /**
     *  Naive implementation copied and adjusted from:
     *  https://stackoverflow.com/questions/14813369/palindrome-check-in-javascript#14813569
     *
     *  Palindrome definition:
     *  https://en.wikipedia.org/wiki/Palindrome
     */
    function isPalindrome(str) {
      return str === str.split('').reverse().join('');
    }

    let palindrome = {
      number:   0,
      factor1:  0,
      factor2:  0
    };

    /*
     * Traverse multiplication table in the following way, n=12 example
     * a) 144, 132, 120, ..., 12
     * b) 121 (palindrome!), 110, ..., 11
     * c) 100, 90, ..., 10
     * d) ...
     * e) 4, 2
     * f) 2
     *
     * If palindrome already found and the number of first product
     * in the column is lower than found palindrome then we stop.
     * There will be no greater number than palindrome.
     *
     * n=12 example. Stop at c) as first product (100) is lower
     * than found palindrome (121).
     *
     * @see https://en.wikipedia.org/wiki/Multiplication_table
     */
    for (let j = upperBound; j > lowerBound; j--) {
      for (let i = upperBound; i > j - 1; i--) {
        if (i === upperBound && i < palindrome.number) {
          return palindrome;
        }

        let product = i * j;
        if (isPalindrome(product + '') && product > palindrome.number) {
          palindrome.number = product;
          palindrome.factor1 = i;
          palindrome.factor2 = j;
        }

      }
    }
    return palindrome;
  }

  return findMaxProductPalindrome(10000, 99999);
}
