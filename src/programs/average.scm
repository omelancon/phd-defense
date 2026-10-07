(define (average lst)
  (let loop ((rest lst) (sum 0) (n 0))
    (if (null? rest)
        #|@div|#(/ sum n)#|@end|#
        (loop #|@cdr|#(cdr rest)#|@end|#
              #|@sum-add|#(+ sum #|@elem|#(car rest)#|@end|#)#|@end|#
              #|@n-add|#(+ n 1)#|@end|#))))

(average '#|@ints|#(90 85 77)#|@end|#)
(average '#|@flos|#(36.6 37.2 38.1)#|@end|#)
