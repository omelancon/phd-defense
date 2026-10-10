(define square
  (hyperfunction
    entries:
      (any: A1
        K: (fx→fx  fl→fl  fx|fl|bg→fx|fl|bg))
      (fx: A2
        K: (fx→fx  #f     fx→bg))
      (fl: A3
        K: (#f     fl→fl))
    blocks:
      A1: (lambda (K x)
            (call *.any×arg[0]
                  fx×arg[0]→fx: K[0]
                  fl×arg[0]→fl: K[1]
                  fx|fl|bg×arg[0]→fx|fl|bg: K[2]
                  x x))
      A2: ...
      A3: ...))
