static int    f_int(int x)    { return x * x + x; }
static double f_dbl(double x) { return x * x + x; }
#define f(x) _Generic((x), int: f_int, double: f_dbl)(x)

#|@answer1|#p(5) // 30 #|@end|#
#|@answer2|#p(10) // 110 #|@end|#
#|@answer3|#p(3.14) // ~12.9996 #|@end|#