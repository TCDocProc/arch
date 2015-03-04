jQuery ->

    class Action extends Backbone.Model

    class Branch extends Backbone.Model

        initialize: (data) ->

            seqs = []

            _.each data.sequences, (seq) =>
                seqs.push new Sequence seq

            @set('seqs',seqs)

    class Sequence extends Backbone.Model

        initialize: (data) ->

            objs = []

            _.each data, (obj) =>
                if obj.type is "action"
                    objs.push new Action obj
                else if obj.type is "branch"
                    objs.push new Branch obj

            @set('objs',objs)

    class Process extends Backbone.Model


    class Processes extends Backbone.Collection

        model: Process
        url: "3.json"

        parse: (response) ->

            _.each response, (process) ->
                process.sequence = new Sequence process.sequence

            return response


###############################################################################

    $(window).on 'popstate', ->

        done = false

        nodes = $(".sequence.fill:not(.hidden)")

        _.each nodes, (node) ->
            if $(node).children(':hidden').length == 0
                $(node).siblings().removeClass "hidden"
                $(node).removeClass "fill"
                done = true

        if not done
            nodes = $(".branch.focused:not(.hidden)")

            _.each nodes, (node) ->
                if $(node).children(':hidden').length == 0 and $(node).parent().hasClass "sequence"
                    $(node).siblings().removeClass "hidden"
                    $(node).removeClass "focused"


    class BranchView extends Backbone.View

        attributes:
            class: "cell branch"

        initialize: ->

            $(@el).click =>

                if $(@el).parent().hasClass 'fill'
                    window.history.pushState 'forward', null, './3.html'
                    $(@el).siblings().addClass "hidden"
                    $(@el).addClass "focused"

        render: ->

            _.each @model.get('seqs'), (seq) =>
                seqView = new SequenceView model: seq
                $(@el).append seqView.render().$el

            return @

    class ActionView extends Backbone.View

        attributes:
            class: "cell action"

        render: ->

            $(@el).addClass @model.get('state')

            $(@el).html "<h1> #{ @model.get("name") } </h1>
                        <p> #{ @model.get("info") } </p>
                        <p> STATUS: #{ @model.get("state") } </p>"

            return @


    class SequenceView extends Backbone.View

        attributes:
            class: "sequence"

        initialize: ->

            $(@el).click =>

                if $(@el).parent().hasClass 'focused'

                    window.history.pushState 'forward', null, './3.html'

                    $(@el).siblings().addClass 'hidden'
                    $(@el).addClass "fill"

        render: ->

            _.each @model.get("objs"), (obj) =>

                switch obj.get("type")
                    when "action"
                        actionView = new ActionView model: obj
                        $(@el).append actionView.render().$el
                    when "branch"
                        branchView = new BranchView model: obj
                        $(@el).append branchView.render().$el

            return @

    class ProcessesView extends Backbone.View

        attributes:
            class: "cell branch focused"

        render: ->

            _.each @collection.models, (proc) =>
                seq = proc.get('sequence')
                processView = new SequenceView model: seq
                $(@el).append processView.render().$el


            return @

    class PageView extends Backbone.View

        el: '.content'

        render: ->
            collection = new Processes
            collection.fetch success: =>
                procView = new ProcessesView collection: collection
                $(@el).append procView.render().$el

    view = new PageView
    view.render()
