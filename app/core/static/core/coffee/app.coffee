jQuery ->


    class Item extends Backbone.Model

        defaults:
            part1: 'Hello'
            part2: 'Backbone'

    class List extends Backbone.Collection

        model: Item

    class ListView extends Backbone.View

        el: $ 'body'

        initialize: ->

            @collection = new List
            @collection.bind 'add', @appendItem

            @counter = 0
            @render()

        render: ->
            $(@el).append '<button id="backbone-test" style="display:none;">Add List Item</button>'
            $(@el).append '<ul></ul>'

        addItem: ->
            @counter++

            item = new Item

            item.set part2: "#{item.get 'part2'} #{@counter}"

            @collection.add item

        appendItem: (item) ->
            $('ul').append "<li>#{item.get 'part1'} #{item.get 'part2'}!</li>"

        events: 'click #backbone-test': 'addItem'

    list_view = new ListView
