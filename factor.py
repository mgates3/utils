#-------------------------------------------------------------------------------
def factor( n ):
    '''
    @return List of prime factors of `n`.
    '''
    factors = []
    for i in range( 2, n//2+1 ):
        while (n % i == 0):
            factors.append( i )
            n = n // i
        if (n == 1):
            break
    if (n != 1 or len( factors ) == 0):
        factors.append( n )
    return factors
# end

#-------------------------------------------------------------------------------
def primes( n ):
    '''
    @return List of primes ≤ `n`.
    '''
    sieve = [1]*(n + 1)
    for i in range( n+1 ):
        sieve[i] = i    
    sieve[1] = 0

    for i in range( 2, n//2+1 ):
        print( f'i {i}' )
        if (sieve[i] != 0):
            j = 2*i
            while (j <= n):
                sieve[ j ] = 0
                j += i
    print( 'sieve:', sieve )
    return list( filter( None, sieve ) )
# end
