/**/

#include <stdio.h>
#include <math.h>

int main()
{

	int one, two, three, four;
	printf("Please enter 4 numbers separated by spaces > ");
	scanf("%d%d%d%d", &one, &two, &three, &four);
	if ((one < two)&&(one < three)&&(one < four))
		printf("%d is the smallest\n", one + 1);
	if ((two < one)&&(two < three)&&(two < four))
		printf("%d is the smallest\n", two + 1);
	if ((three < one)&&(three < two)&&(three < four))
		printf("%d is the smallest\n", three + 1);
	if ((four < one)&&(four < two)&&(four < three))
		printf("%d is the smallest\n", four + 1);
	return(0);
}		
