
//
/**
*Fibonacci   F1=1 F2=1  Fn=Fn-1+Fn-2 (n>2)
**/



class FreshJuice{

	enum FreshJuiceSize{Small, Medium, Large}
	FreshJuiceSize size;
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

	}
}