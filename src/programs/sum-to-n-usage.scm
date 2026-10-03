(define (sum-to-n n)
  (let loop ((i 1) (sum 0))
    (if (> i n)
        sum
        (loop (+ i 1) (+ sum i)))))

(let ((i (sum-to-n 3)))
  (display (vector-set v i)))