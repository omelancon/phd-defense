(define (fib n)
  (if #|@le|#(<= n 1)#|@end|#
      n
      #|@plus|#(+ (fib #|@sub1|#(- n 1)#|@end|#) (fib #|@sub2|#(- n 2)#|@end|#))#|@end|#))
