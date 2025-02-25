using System;

namespace homework
{ 
    class Task
    {
        static bool IsPrime(int upperBound) //checks for prime number and returns a boolean value.
        {
            if(upperBound <=1)
            {
                return false;
            }
            for (int i = 2; i < upperBound; i++)
            {
                if(upperBound%i==0)
                {
                    return false;
                }
            }
            return true;
        }
        static void Main (string[] args)
        {
            int upperBound = 1; //gives error if they are not assigned, value assignment 
            int lowerBound = 1;//in try catch blocks are not taken as granted by program.

            Console.WriteLine("Check the prime numbers in between two digits. Be nice and don't input anything funny,just positive integers, OK?");
            try
            {
                Console.WriteLine("Enter the starting number:");
                lowerBound = Convert.ToInt32(Console.ReadLine());
                Console.WriteLine("Enter the ending number:");
                upperBound = Convert.ToInt32(Console.ReadLine());
                Console.WriteLine("Prime numbers between " + upperBound + " and " + lowerBound + " are:");
            }
            catch (Exception e)
            {
                Console.WriteLine("You entered something weired,didn't you?");
            }

            int adjoustedUpperBound = upperBound - 1;

            int count = 1;
            while( adjoustedUpperBound>lowerBound)
            {
                if(IsPrime(adjoustedUpperBound)==false)
                {
                    adjoustedUpperBound--;
                    
                }
                else
                {
                    Console.Write(adjoustedUpperBound+" ");
                    adjoustedUpperBound--;
                    if(count%10 == 0)
                    {
                        Console.WriteLine();
                    }
                    count++;
                }
                
       
            }
           
          
           
        }
    }
}

