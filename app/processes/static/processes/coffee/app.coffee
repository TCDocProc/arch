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



    class BranchView extends Backbone.View

        attributes:
            class: "branch"
            style: "overflow-x: scroll; display: block"

        render: ->

            _.each @model.get('seqs'), (seq) =>
                seqView = new SequenceView model: seq
                $(@el).append seqView.render().$el
                seqView.$el.css('width',""+(100/@model.get('seqs').length-10)+"%")

            return @

    class ActionView extends Backbone.View

        attributes:
            class: "action"
            style: "display:block; height:100px; border-radius: 5px; border: 1px solid black; padding: 10px"

        render: ->

            $(@el).html "<p> #{ @model.get("name") } </p>"
            return @


    class SequenceView extends Backbone.View

        attributes:
            class: "sequence"
            style: "display:inline-block;
                    width:90%;
                    margin: 5%;
                    border-radius:5px;
                    background-color: #666666;
                    vertical-align: top"

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
            class: "process"
            style: "overflow-x: scroll; white-space:nowrap; max-height:100%;"

        render: ->

            _.each @collection.models, (proc) =>
                seq = proc.get('sequence')
                processView = new SequenceView model: seq
                $(@el).append processView.render().$el

            return @

    class PageView extends Backbone.View

        el: 'body'

        render: ->
            collection = new Processes
            collection.fetch success: =>
                procView = new ProcessesView collection: collection
                $(@el).append procView.render().$el

    view = new PageView
    view.render()
