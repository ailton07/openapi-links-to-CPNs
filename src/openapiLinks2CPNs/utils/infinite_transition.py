from snakes.plugins import plugin, new_instance
from snakes.data import MultiSet

@plugin("snakes.nets")
def extend (module) :
    class Transition (module.Transition) :
        """ 
        This is a special module. When loaded, the transitions doens't consome input tokens.
        To achieve this effect, we overwrighted the fire method
        """
    # "Extends `module`"
        def fire (self, binding) :
            #Original code in https://github.com/fpom/snakes/blob/4b98f2bac679222fc28b3de538090d2373e214c8/snakes/nets.py#L2655
            """Fire the transition with `binding`.
            >>> t = Transition('t', Expression('x!=1'))
            >>> px = Place('px', range(3))
            >>> t.add_input(px, Variable('x'))
            >>> py = Place('py')
            >>> t.add_output(py, Expression('x+1'))
            >>> t.fire(Substitution(x=0))
            >>> px.tokens == MultiSet([1, 2])
            True
            >>> py.tokens == MultiSet([1])
            True
            >>> try : t.fire(Substitution(x=1))
            ... except ValueError : print(sys.exc_info()[1])
            transition not enabled for {x -> 1}
            >>> t.fire(Substitution(x=2))
            >>> px.tokens == MultiSet([1])
            True
            >>> py.tokens == MultiSet([1, 3])
            True
            @param binding: a substitution from variables to values (not
                variables)
            @type binding: `Substitution`§
            @raise ValueError: when the provided binding does not enable
                the transition
            """
            if self.enabled(binding) :
                # for place, label in self.input() :
                #     place.remove(label.flow(binding))
                for place, label in self.output() :
                    multiset = label.flow(binding)
                    if multiset.size() > 0 and type(multiset.items()) == list \
                    and type(multiset.items()[0]) == MultiSet  and len(multiset.items()[0].items()) > 1:
                        self.handle_multiple_tokens(place, multiset)
                        return
                    place.add(label.flow(binding))
            else :
                raise ValueError("transition not enabled for %s" % binding)
            
        def handle_multiple_tokens(self, place, multiset):
            
            for item in multiset.items()[0].items():
                place.add(MultiSet(item))
        
    return Transition


    

    