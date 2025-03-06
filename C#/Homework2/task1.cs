using System;
using System.Collections.Generic;

abstract class Shape
{
    public abstract double GetArea();  // Compute Surface Area
    public abstract bool IsValid();    // Check Validity of attributes
    public abstract string GetShapeType(); // To Get the shape type
}

class Rectangle : Shape
{
    private double width;
    private double height;

    public Rectangle(double width, double height)
    {
        this.width = width;
        this.height = height;
    }

    public override double GetArea()
    {
        return IsValid() ? width * height : 0;
    }
    public override bool IsValid()
    {
        return width > 0 && height > 0;
    }
    public override string GetShapeType()
    {
        return "Rectangle";
    }
}

class Square : Shape
{
    private double side;

    public Square(double side)
    {
        this.side = side;
    }

    public override double GetArea()
    {
        return IsValid() ? side * side : 0;
    }
    public override bool IsValid()
    {
        return side > 0;
    }
    public override string GetShapeType()
    {
        return "Square";
    }
}

class Circle : Shape
{
    private double radius;

    public Circle(double radius)
    {
        this.radius = radius;
    }

    public override double GetArea()
    {
        return IsValid() ? Math.PI * radius * radius : 0;
    }
    public override bool IsValid()
    {
        return radius > 0;
    }
    public override string GetShapeType()
    {
        return "Circle";
    }
}

class Cylinder : Shape
{
    private double radius;
    private double height;

    public Cylinder(double radius, double height)
    {
        this.radius = radius;
        this.height = height;
    }

    public override double GetArea()
    {
        return IsValid() ? 2 * Math.PI * radius * height : 0;
    }
    public override bool IsValid()
    {
        return radius > 0 && height > 0;
    }
    public override string GetShapeType()
    {
        return "Cylinder";
    }
}

class Program
{

    static void Main()
    {
        List<Shape> shapes = new List<Shape>();
        Random random = new Random();

       
        for (int i = 0; i < 10; i++)
        {
            double height = random.Next(-1,6); // Height between -1 and 5
            double width = random.Next(-1,6);  // Width between -1 and 5
            double radius = random.Next(-1,6); // radius between -1 and 5

            Shape shape = new Rectangle(1, 1);
            int shapeChoice = random.Next(4); // Random number between 0 and 3
            switch (shapeChoice)
            {
                case 0:
                    shape = new Rectangle(width, height);
                    break;
                case 1:
                    shape = new Square(height); // Using height as side for square
                    break;
                case 2:
                    shape = new Circle(radius);
                    break;
                case 3:
                    shape = new Cylinder(radius, height);
                    break;
            }

            
            shapes.Add(shape);
            if(!shape.IsValid())
            {
                Console.WriteLine($"Not a valid shape for {shape.GetShapeType()}");
            }
            else
            {
                Console.WriteLine($"Area of {shape.GetShapeType()} is: {shape.GetArea():F2}");
            }
          
       
        }

        // Calculate the total area of all shapes
        double totalArea = 0;
        foreach (var shape in shapes)
        {
           if(shape.IsValid())
            {
                totalArea += shape.GetArea();
            }
            
        }
        Console.WriteLine($"Total area of all valid shapes: {totalArea:F2}");
    }
}
