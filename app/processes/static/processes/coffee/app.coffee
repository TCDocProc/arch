jQuery ->

    class Action extends Backbone.Model

    class Branch extends Backbone.Model

        initialize: (data) ->

            seqs = []

            _.each data.sequences, (seq, i) =>
                s = new Sequence seq
                s.i = i
                seqs.push s

            @set('seqs',seqs)

    class Sequence extends Backbone.Model

        initialize: (data) ->

            objs = []

            _.each data, (obj,i) =>
                if obj.type is "action"
                    a = new Action obj
                    a.i = i
                    objs.push a

                else if obj.type is "branch"
                    b = new Branch obj
                    b.i = i
                    objs.push b

            @set('objs',objs)

    class Process extends Backbone.Model


    class Processes extends Backbone.Collection

        model: Process

        url: ->

            "/processes/user/#{@user_id}.json"

        initialize: (user_id) ->

            @user_id = user_id
            return @

        parse: (response) ->

            _.each response, (process,i) ->
                s = new Sequence process.sequence
                s.i = i
                process.sequence = s
                process.i = i

            return response


###############################################################################

    class ActionView extends Backbone.View

        attributes:
            class: "cell action"

        setup: (siblingCount) ->

            $(@el).addClass("siblings-#{siblingCount}")

        render: ->

            $(@el).addClass @model.get('state')

            $(@el).html "<h1> #{ @model.get("name") } </h1>" +
                        "<p> #{ @model.get("info") } </p>" +
                        "<p> STATUS: #{ @model.get("state") } </p>"

            return @

        moveToPath: (path) ->

            if _.first(path)? and _.first(path) isnt @model.i
                $(@el).hide()
            else
                $(@el).show()


    class BranchView extends Backbone.View

        attributes:
            class: "cell branch"

        setup: (siblingCount) ->

            $(@el).addClass "siblings-#{siblingCount}"
            $(@el).addClass "children-#{@model.get("seqs").length}"
            $(@el).click =>
                if $(@el).parent().hasClass('fill') and not $(@el).hasClass("focused")
                    Backbone.history.navigate "#{Backbone.history.fragment.match(/.*[^\/]/g)}/#{@model.i}", true

        render: ->

            @childViews = []

            _.each @model.get('seqs'), (seq) =>
                seqView = new SequenceView model: seq
                seqView.setup @model.get('seqs').length
                $(@el).append seqView.render().$el
                @childViews.push(seqView)

            return @

        moveToPath: (path) ->


            passToChildren = =>

                @childViews.map (view) =>
                    nextPath = undefined
                    nextPath = _.tail(path) if path?
                    view.moveToPath nextPath

            if _.first(path)?

                if _.first(path) is @model.i

                    $(@el).addClass "focused"
                    $(@el).addClass "remove-width"

                    passToChildren()
                else

                    $(@el).hide()
            else

                    $(@el).removeClass "remove-width"
                    $(@el).removeClass "focused"
                    $(@el).show()

                    passToChildren()


    class SequenceView extends Backbone.View

        attributes:
            class: "sequence"

        visible: true

        setup: (siblingCount, header) ->

            $(@el).addClass "siblings-#{siblingCount}"
            $(@el).addClass "children-#{@model.get("objs").length}"
            $(@el).prepend  "<h1>#{header}</h1>" if header isnt undefined
            $(@el).click =>
                if $(@el).parent().hasClass('focused') and not $(@el).hasClass("fill")
                    Backbone.history.navigate "#{Backbone.history.fragment.match(/.*[^\/]/g)}/#{@model.i}", true

        render: ->

            @childViews = []

            _.each @model.get("objs"), (obj) =>

                switch obj.get("type")

                    when "action"
                        actionView = new ActionView model: obj
                        actionView.setup @model.get("objs").length
                        $(@el).append actionView.render().$el
                        @childViews.push(actionView)

                    when "branch"
                        branchView = new BranchView model: obj
                        branchView.setup @model.get("objs").length
                        $(@el).append branchView.render().$el
                        @childViews.push(branchView)

            return @

        moveToPath: (path) ->


            passToChildren = =>

                @childViews.map (cell) =>
                    nextPath = undefined
                    nextPath = _.tail(path) if path?
                    cell.moveToPath nextPath


            if _.first(path)?

                if _.first(path) is @model.i
                    $(@el).addClass "fill"
                    $(@el).children('.action').children('p').show()
                    passToChildren()

                else

                    $(@el).hide()
            else

                $(@el).children('.action').children('p').hide()
                $(@el).removeClass "fill"
                $(@el).show()
                
                passToChildren()



    class ProcessesView extends Backbone.View

        attributes:
            class: "cell branch focused remove-width"

        initialize: (collection) ->

            @collection = collection
            return @

        render: ->

            @childViews = []

            $(@el).addClass "children-#{@collection.models.length}"
            _.each @collection.models, (proc) =>
                seq = proc.get('sequence')
                processView = new SequenceView model: seq
                processView.setup @collection.models.length, proc.get('name')
                $(@el).append processView.render().$el
                @childViews.push processView

            return @

        moveToPath: (path) ->

            completion = 0
            @childViews.map (view) =>
                view.moveToPath path

    class PageView extends Backbone.View

        el: '.content'

        initialize: (user_id) ->

            @user_id = user_id
            $('ul.title-area > :nth-child(1)').click =>
                Backbone.history.navigate "/processes/user/#{@user_id}", true

            return @

        render: (callback) ->

            collection = new Processes @user_id

            collection.fetch success: =>
                @procView = new ProcessesView collection
                $(@el).html @procView.render().$el
                callback()

            return @

        moveToPath: (path) ->

            navClick = (path) =>
                Backbone.history.navigate "/processes/user/#{@user_id}/#{path.join('/')}", true

            $('ul.title-area > :not(:nth-child(1))')?.remove()

            pathArray = path?.split("/").map(Number)

            pathArray?.forEach (e, i) =>

                if i is 0
                    $('ul.title-area').append "<li class='name'><h1>&#10095;</h1></li><li class='name'><h1><a>" + $(".content > .branch").children().eq(e).children("h1").text() + "</a></h1></li>"
                else
                    $('ul.title-area').append "<li class='name'><h1>&#10095;</h1></li><li class='name'><h1><a>...</a></h1></li>"

                $('ul.title-area').children(":last-child").click -> navClick(_.first(pathArray,i+1))

            @procView.moveToPath pathArray

    class AppRouter extends Backbone.Router

        routes:
            "processes/user/:user_id(/*path)": "process"

    app_router = new AppRouter;

    view = undefined

    app_router.on 'route:process',  (user_id, path) ->

        if view?
            view.moveToPath path
        else
            view = new PageView user_id
            view.render ->
                view.moveToPath path

    Backbone.history.start pushState: true
