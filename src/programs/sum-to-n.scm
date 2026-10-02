(define (sum-to-n n)
  (let loop (#|@i-init|# (i 0) #|@end|# #|@sum-init|# (sum 0) #|@end|#)
    (if #|@n-test|# (> i n) #|@end|#
        #|@result|# sum #|@end|#
        (loop #|@i-step|# (+ i 1) #|@end|# #|@sum-step|# (+ sum i) #|@end|#))))
