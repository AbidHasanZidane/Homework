using System;

namespace homework
{ 
    class Task
    {
        static void Main (string[] args)
        {
            int upperBound =10;
            int lowerbound = 2;
            Console.WriteLine("Check the whole numbers in between two digits, be nice and don't input anything funny, OK?");
            Console.WriteLine("Enter the starting number:");
            lowerbound = Convert.ToInt32(Console.ReadLine());
            Console.WriteLine("Enter the ending number:");
            upperBound = Convert.ToInt32(Console.ReadLine());
            Console.WriteLine("Numbers between " +lowerbound+" and "+ upperBound+" is: ");
            for (int i = lowerbound; i<upperBound-1; )
            {
                Console.WriteLine(++i);
            }
        }
    }
}

