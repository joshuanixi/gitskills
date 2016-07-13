
//
/**
*Fibonacci   F1=1 F2=1  Fn=Fn-1+Fn-2 (n>2)
**/



class FreshJuice{

	enum FreshJuiceSize{Small, Medium, Large}
	FreshJuiceSize size;
}

class FatherClass{


    FatherClass(){
    	System.out.println("Father construction method");
    }
	public int value;
	public void f(){
		value=100;
		System.out.println("Fatherclass.value:"+value);


	}
}

class ChildClass extends FatherClass{

	ChildClass(){
    	System.out.println("Child construction method");
    }

	public int value;
	public void f(){

		super.f();
		value=200;
		System.out.println("ChildClass.value:"+value);
		System.out.println(value);
		System.out.println(super.value);
	}




}

class BirthDate{
	private int day;
	private int month;
	private int year;
	public BirthDate(int d, int m,int y){
		day=d;
		month=m;
		year=y;
	}

	public void setDay(int d) {day=d;}
	public void setMonth(int m){month=m;}
	public void setyear(int y){year=y;}

	public int getDay(){return day;}
	public int getMonth(){return month;}
	public int getYear(){return year;}

	public void display(){

		System.out.println("Your birthday is "+day+"/"+month+"/"+year);
	}





}




public class FreshJuiceTest{

	public static int methon(int n){

		if(n==1)
			return 1;
		else
			return n*methon(n-1);
	} 


	public static int Fibonacci(int n){


		if(n<=2)
			return 1;
		else
			return Fibonacci(n-1)+Fibonacci(n-2);


	}

	public static void main(String args[]){


		FreshJuice juice=new FreshJuice();
		juice.size=FreshJuice.FreshJuiceSize.Medium;
		System.out.println("size:" +juice.size);
		System.out.println(methon(5));
		System.out.println(Fibonacci(1));
		System.out.println(Fibonacci(2));
		System.out.println(Fibonacci(3));
		System.out.println(Fibonacci(4));
		System.out.println(Fibonacci(10));


		BirthDate birthdate=new BirthDate(8,01,1988);
        birthdate.display();


        ChildClass child=new ChildClass();
        child.f();



	}
}